from typing import Union

from loguru import logger
from telebot.types import CallbackQuery, Message

from customer.models import User
from tbot.messages import Messages
from tbot.storage import storage
from tbot_messages.bot import bot


@bot.message_handler(
    func=lambda mess: User.objects.filter(chat_id=mess.chat.id,
                                          blocked=True).exists()
)
@bot.callback_query_handler(
    func=lambda call: User.objects.filter(chat_id=call.message.chat.id,
                                          blocked=True).exists()
)
def user_block(mess: Union[Message, CallbackQuery]):
    logger.debug(f'Block {mess.from_user.id}')


@bot.message_handler(is_reply_btn_click=Messages.NotFoundNews.buttons[1])
@bot.message_handler(
    is_reply_btn_click=Messages.NotFoundNewsUnsubscribe.buttons[1]
)
@bot.message_handler(is_reply_btn_click=Messages.DetailNews.buttons[1])
@bot.message_handler(is_reply_btn_click=Messages.SupportAsk.buttons[1])
@bot.message_handler(is_reply_btn_click=Messages.ThxForQuestion.buttons[1])
@bot.message_handler(is_reply_btn_click=Messages.Agreement.buttons[1])
@bot.message_handler(is_reply_btn_click=Messages.Profile.buttons[6])
@bot.message_handler(is_reply_btn_click=Messages.MySubscribe.buttons[0])
@bot.message_handler(is_reply_btn_click=Messages.Assistant.buttons[1])
@bot.message_handler(is_reply_btn_click=Messages.Name.buttons[1])
@bot.message_handler(is_reply_btn_click=Messages.NameNotSet.buttons[1])
@bot.message_handler(is_reply_btn_click=Messages.DepartDate.buttons[1])
@bot.message_handler(is_reply_btn_click=Messages.DocumentsIdNumber.buttons[1])
@bot.message_handler(is_reply_btn_click=Messages.DocumentsCertificateSeries
                     .buttons[1])
@bot.message_handler(is_reply_btn_click=Messages.DocumentsCertificateNumber
                     .buttons[1])
@bot.message_handler(
    is_reply_btn_click=Messages.DocumentsBookSeries.buttons[1])
@bot.message_handler(
    is_reply_btn_click=Messages.DocumentsBookNumber.buttons[1])
@bot.message_handler(is_reply_btn_click=Messages.DocumentStart.buttons[0])
@bot.message_handler(is_reply_btn_click=Messages.InactiveStart.buttons[0])
@bot.message_handler(is_reply_btn_click=Messages.Enter_car_number.buttons[1])
@bot.message_handler(is_reply_btn_click=Messages.Enter_car_series.buttons[1])
@bot.message_handler(is_reply_btn_click=Messages.Fines_Start.buttons[0])
@bot.message_handler(
    is_reply_btn_click=Messages.FinesResultNotFound.buttons[0])
@bot.message_handler(is_reply_btn_click=Messages.StateRegisters.buttons[8])
@bot.message_handler(is_reply_btn_click=Messages.MonitoringNational.buttons[1])
@bot.message_handler(is_reply_btn_click=Messages.MonitoringStart.buttons[0])
@bot.message_handler(commands=['start'])
@bot.callback_query_handler(func=lambda call: call.data == 'menu')
def start_message(message: Union[Message, CallbackQuery]):
    if type(message) == CallbackQuery:
        message.message.from_user = message.from_user
        message = message.message
    user, add = User.objects.update_or_create(
        chat_id=message.chat.id,
        defaults={
            'username': message.from_user.username,
        }
    )
    storage.set_user_state(message.chat.id, '')
    if add:
        storage.set_user_data(message.chat.id, {'locale': 'en'})
        Messages.Start.send_if_active(message.chat.id)
        Messages.Lang.send_if_active(message.chat.id)
    else:
        storage.set_user_data(
            message.chat.id,
            {'locale': user.language if user.language != 'ru' else None}
        )
        Messages.Menu.send_if_active(message.chat.id, set_state='')


@bot.message_handler(commands=['language'])
@bot.message_handler(is_reply_btn_click=Messages.Profile.buttons[0])
def language_message(message: Message):
    Messages.Lang.send_if_active(message.chat.id)
