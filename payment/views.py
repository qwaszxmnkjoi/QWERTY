from datetime import timedelta
from urllib.parse import parse_qsl

from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from loguru import logger

from customer.models import User
from tbot.messages import Messages
from tbot_messages.bot import bot
from .payment import service


@csrf_exempt
def get_payment(request, backend: str = 'liqpay'):
    if request.method == 'POST':
        if backend == 'liqpay':
            post = request.POST
            data = post.get('data')
            signature = post.get('signature')

            my_sign = service.lqp.str_to_sign(service.lqp.private_key + data + service.lqp.private_key)
            resp = service.lqp.decode_data_from_str(data)
            logger.debug(logger)

            if my_sign == signature and resp['status'] == 'subscribed':
                message_id, chat_id = resp.get('info', '123_123').split('_')

                try:
                    bot.delete_message(chat_id, message_id)
                except Exception as e:
                    pass

                user, add = User.objects.get_or_create(chat_id=chat_id)
                if add or user.role == 'client':
                    user.role = 'expert'
                    user.subs_id = resp.get('order_id', None)
                    user.date_end = timezone.now() + timedelta(days=30)
                    user.save()
                    Messages.PaySub.send_if_active(
                        chat_id, format_map={
                            'card': resp.get('sender_card_mask2'),
                            'cost': resp.get('amount')
                        }
                    )
                else:
                    user.date_end = user.date_end + timedelta(days=30)
                    user.subs_id = resp.get('order_id', None)
                    user.save()
                    Messages.PayContinueSub.send_if_active(
                        chat_id, format_map={'date': user.date_end.date()}
                    )

            return HttpResponse('Done!')
        else:
            data = request.body.decode('utf-8')
            data = dict(parse_qsl(data))
            logger.debug(data)

            order_id = data.get('SHOPBILLID')  # Portmone Number
            bill_number = data.get('SHOPORDERNUMBER')    # Emigrant NUmber

            message_id = data.get('ATTRIBUTE1')
            chat_id = data.get('ATTRIBUTE2')
            try:
                bot.delete_message(chat_id, message_id)
            except Exception as e:
                logger.debug(e)

            user, add = User.objects.get_or_create(chat_id=chat_id)
            if add or user.role == 'client':
                user.role = 'expert'
                user.subs_id = order_id
                user.date_end = timezone.now() + timedelta(days=30)
                user.save()
                Messages.PaySub.send_if_active(
                    chat_id, format_map={
                        'card': data.get('CARD_MASK'),
                        'cost': data.get('BILL_AMOUNT')
                    }
                )
            else:
                user.date_end = user.date_end + timedelta(days=30)
                user.subs_id = order_id
                user.save()
                Messages.PayContinueSub.send_if_active(
                    chat_id, format_map={'date': user.date_end.date()}
                )
            return HttpResponsePermanentRedirect(f'https://t.me/{bot.get_me().username}')
    else:
        return HttpResponse('Уффф...')
