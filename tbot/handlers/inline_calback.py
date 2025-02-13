from customer.models import User
from tbot.messages import Messages
from tbot.storage import storage
from tbot_messages.bot import bot


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    data = call.data
    if data.startswith('language#'):
        lang = data.split('#')[-1]
        storage.update_user_data(call.message.chat.id, 'locale',
                                 None if lang == 'ru' else lang)
        User.objects.update_or_create(
            chat_id=call.message.chat.id,
            defaults={
               'language': lang,
            }
        )
        Messages.Menu.send_if_active(call.message.chat.id)
