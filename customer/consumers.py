import typing

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.core.files.base import ContentFile

from customer.models import Message, MessageDocument
from .serializers import ModelSerializer


def get_messages(category_id: int, limit: int = 10, page: int = 1) -> typing.Tuple[typing.List[typing.Dict[str, typing.Any]], bool]:
    result = Message.objects.filter(category_id=category_id).order_by('-dt_create').prefetch_related('document')
    finish = page * limit
    start = finish - limit
    is_next = result.count() > finish  # or result(Serialized) len >= limit
    result = ModelSerializer(queryset=result[start:finish]).as_json()
    return result, is_next


class ChatConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = {}

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        if bytes_data:
            self.receive_files(bytes_data)
        else:
            self.receive_json(self.decode_json(text_data), **kwargs)

    def receive_json(self, content, **kwargs):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        command = content.get('command', None)
        try:
            data = content.get('data')
            if command == 'set_session':
                channel_ses = content.get('session')
                session = self.session.setdefault(self.channel_name, channel_ses)
                if channel_ses.get('file'):
                    session['file'] = channel_ses['file']
            elif not data:
                return self.send_json({'error': 'data must be specified'})
            elif command == 'init':
                self.init_message(data, data['category_id'])
            elif command == 'load_more':
                self.load_more(data)
            elif command == 'send':
                self.send_msg(data, data['category_id'])
            elif command == 'send_doc':
                self.send_doc_msg(data, data['category_id'])
        except Exception as e:
            # Catch any errors and send it back
            self.send_json({"error": str(e)})

    def init_message(self, data, category_id: int):
        self.groups.append(f'cat-{category_id}')
        async_to_sync(self.channel_layer.group_add)(f'cat-{category_id}', self.channel_name)

        messages, is_next = get_messages(category_id, int(data.get('limit', 10)))
        self.send_json({
            'messages': messages,
            'is_next': is_next,
            'is_init': True,
            'command': 'add_message'
        })

    def load_more(self, data):
        messages, is_next = get_messages(data['category_id'], int(data.get('limit', 10)), int(data.get('page', 1)))
        self.send_json({
            'messages': messages,
            'is_next': is_next,
            'is_init': False,
            'command': 'load_more'
        })

    def send_msg(self, data, category_id: int):
        messages = self.create_message(category_id=category_id, data=data)
        data = {
            'messages': messages,
            'is_init': False,
            'command': 'add_message'
        }
        data = {"type": "send_one", "text": self.encode_json(data)}
        async_to_sync(self.channel_layer.group_send)(
            f'cat-{category_id}', data
        )

    def send_doc_msg(self, data, category_id: int):
        channel_ses = self.session.get(self.channel_name) or {}
        if channel_ses:
            data.update({
                'files': channel_ses.get('files'),
                'images': channel_ses.get('images'),
            })
            messages = self.create_message(category_id=category_id, data=data)
            result = {
                'messages': messages,
                'is_init': False,
                'command': 'add_message'
            }
            result = {"type": "send_one", "text": self.encode_json(result)}
            async_to_sync(self.channel_layer.group_send)(
                f'cat-{category_id}', result
            )
        self.session.pop(self.channel_name)

    def send_one(self, data):
        self.send(data['text'])

    def receive_files(self, file):
        channel_ses = self.session.get(self.channel_name, {})
        if channel_ses:
            file_data = channel_ses.get('file')
            if file_data.get('is_file', False):
                key = 'files'
            else:
                key = 'images'
            objs = channel_ses.setdefault(key, [])
            objs.append(ContentFile(file, file_data.get('name')))
            channel_ses[key] = objs

    @classmethod
    def create_message(cls, category_id: int, data: dict):
        msg = Message(
            category_id=category_id,
            user_id=data.get('user_id'),
            text=data.get('text')
        )
        msg.save()
        document_data = []
        if files := data.get('files', []):
            document_data.extend([MessageDocument(message=msg, src_file=obj) for obj in files])
        if images := data.get('images', []):
            document_data.extend([MessageDocument(message=msg, src_image=obj) for obj in images])

        MessageDocument.objects.bulk_create(document_data)
        result = ModelSerializer(queryset=[msg]).as_json()
        return result


chat_consumer = ChatConsumer.as_asgi()
