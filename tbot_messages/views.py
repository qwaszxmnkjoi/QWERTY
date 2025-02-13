import loguru
from django.conf import settings
from django.core.exceptions import RequestAborted
from django.http import HttpResponse
from django.utils.translation import activate
from django.views.decorators.csrf import csrf_exempt
from telebot.types import Update, User as TbotUser

from customer.models import User
from .bot import bot

for module in settings.BOT_HANDLERS:
    __import__(module)


@csrf_exempt
def webhook(request):

    def path_tg_user(chat_id: int, tg_user: TbotUser):
        User.objects.update_or_create(chat_id=chat_id, defaults={'tg_data': tg_user.to_dict()})

    def set_language(lang: str, tg_user: TbotUser):
        activate(lang if lang != 'ua' else 'uk')
        setattr(tg_user, 'lang', lang)
        return tg_user

    if request.META.get('CONTENT_TYPE', 'undef') == 'application/json':
        json_data = request.body.decode('utf-8')
        loguru.logger.debug(json_data)
        update = Update.de_json(json_data)
        if update.message:
            message = update.message
            user_id = message.from_user.id
            user_state = settings.BOT_STORAGE.get_user_state(user_id)

            path_tg_user(user_id, message.from_user)

            # todo: use .dialog and .dialog_stage
            # pushing state directly to message object
            message.from_user.state = user_state

            locale = settings.BOT_STORAGE.get_user_data(user_id).get('locale', None)
            set_language(locale, message.from_user)

            # proceeding custom message object
            bot.process_new_messages([message])
        elif update.callback_query:
            callback = update.callback_query
            user_id = callback.from_user.id
            user_state = settings.BOT_STORAGE.get_user_state(user_id)

            path_tg_user(user_id, callback.from_user)

            # todo: use .dialog and .dialog_stage
            # pushing state directly to message object
            callback.from_user.state = user_state

            locale = settings.BOT_STORAGE.get_user_data(user_id).get('locale', None)
            set_language(locale, callback.from_user)

            # proceeding custom message object
            bot.process_new_callback_query([callback])
        elif update.inline_query:
            inline_query = update.inline_query
            user_id = inline_query.from_user.id
            user_state = settings.BOT_STORAGE.get_user_state(user_id)

            path_tg_user(user_id, inline_query.from_user)

            inline_query.from_user.state = user_state
            locale = settings.BOT_STORAGE.get_user_data(user_id).get('locale', None)
            set_language(locale, inline_query.from_user)

            bot.process_new_inline_query([inline_query])
        elif update.chosen_inline_result:
            chosen_inline_result = update.chosen_inline_result
            user_id = chosen_inline_result.from_user.id
            user_state = settings.BOT_STORAGE.get_user_state(user_id)

            path_tg_user(user_id, chosen_inline_result.from_user)

            chosen_inline_result.from_user.state = user_state
            locale = settings.BOT_STORAGE.get_user_data(user_id).get('locale', None)
            set_language(locale, chosen_inline_result.from_user)
            bot.process_new_chosen_inline_query([chosen_inline_result])
        else:
            bot.process_new_updates([update])

        return HttpResponse(status=200)
    else:
        raise RequestAborted
