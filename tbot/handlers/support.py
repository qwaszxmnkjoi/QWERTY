from typing import Union

from bs4 import BeautifulSoup
from django.conf import settings
from loguru import logger
from telebot.types import CallbackQuery, Message

from customer.models import User
from tbot.messages import Dialogs, Messages
from tbot_messages.bot import bot
from tbot_messages.utils import is_state


@bot.message_handler(
    func=lambda message: message.reply_to_message and User.objects.filter(
        chat_id=message.chat.id,
        role='support'
    ).exists() is True)
def support_reply(message: Message):
    soup = BeautifulSoup(message.reply_to_message.html_text,
                         features='html.parser')
    code = soup.find_all('code')
    if len(code) == 2:
        try:
            bot.send_message(code[1].text, 'SUPPORT:\n' + message.text,
                             reply_to_message_id=code[0].text)
        except Exception as e:
            if 'replied message not found' in str(e):
                bot.send_message(code[1].text, 'SUPPORT:\n' + message.text)


@bot.message_handler(is_reply_btn_click=Messages.Menu.buttons[4])
@bot.message_handler(
    func=is_state('SUPPORT:SupportAsk'),
    is_reply_btn_click=Messages.SupportAsk.buttons[0]
)
@bot.message_handler(
    func=is_state('SUPPORT:Agreement'),
    is_reply_btn_click=Messages.Agreement.buttons[0]
)
def support_message(message: Message):
    Dialogs.SUPPORT.next_message(message.chat.id, index=0)


@bot.message_handler(
    func=is_state('SUPPORT:ThxForQuestion'),
    is_reply_btn_click=Messages.ThxForQuestion.buttons[0]
)
@bot.callback_query_handler(
    func=lambda call:
    call.from_user.state == 'SUPPORT:Support' and call.data == 'ask'
)
def support_ask(call: Union[CallbackQuery, Message]):
    logger.info(call.from_user.state)
    if type(call) == CallbackQuery:
        logger.debug(call.message.text)
        Dialogs.SUPPORT.next_message(call.message.chat.id)
    else:
        logger.debug(call.text)
        Dialogs.SUPPORT.previous_message(call.chat.id)


@bot.callback_query_handler(
    func=lambda call: is_state('SUPPORT:Support') and call.data == 'agreement'
)
def support_agreement(call: CallbackQuery):
    try:
        with open(settings.MEDIA_ROOT / 'agreement.docx', 'rb') as agreement_file:
            Messages.Agreement.send_if_active(
                user_id=call.message.chat.id,
                file=agreement_file,
                set_state='SUPPORT:Agreement'
            )
        with open(settings.MEDIA_ROOT / 'policy.docx', 'rb') as policy_file:
            Messages.Agreement.send_if_active(
                user_id=call.message.chat.id,
                file=policy_file,
                custom_text='',
                set_state='SUPPORT:Agreement'
            )
    except Exception as e:
        logger.debug(e)
        Messages.Agreement.send_if_active(
            user_id=call.message.chat.id,
            set_state='SUPPORT:Agreement'
        )


@bot.message_handler(
    func=lambda message: message.from_user.state == 'SUPPORT:SupportAsk'
)
def user_send_message(message: Message):
    Dialogs.SUPPORT.next_message(message.chat.id)

    lang = {None: 'Русский', 'en': 'Английский', 'ua': 'Украинский'}

    text = 'Поступил вопрос от <a href="tg://user?id={}">{}</a>' \
           '\nЯзык Общения: {}' \
           '\nID Сообщения: <code>{}</code>' \
           '\nChatId Пользователя: <code>{}</code>' \
           '\n\n⚠️Чтобы ответить пользователю сформируйте ответ ссылаясь на ' \
           'Это сообщение⚠️'.format(message.chat.id,
                                    message.from_user.full_name,
                                    lang[message.from_user.lang],
                                    message.message_id,
                                    message.chat.id
                                    )

    support = User.objects.filter(role='support')
    support = support.last() if support else None

    bot.send_message(support.chat_id, text)
    bot.send_message(support.chat_id, message.text)
