import typing

from loguru import logger
from telebot.types import CallbackQuery, Message

from customer.enums import State
from customer.models import Bdr, User, SavedSearch
from customer.tasks import scrap_fines
from tbot.messages import Dialogs, Messages
from tbot.storage import storage
from tbot_messages.bot import bot
from tbot_messages.utils import is_data, is_state


@bot.callback_query_handler(func=is_data('monitoring#fines'))
@bot.message_handler(func=is_state('FINES:Enter_car_series'),
                     is_reply_btn_click=Messages.Enter_car_series.buttons[0])
def fines_message(msg: typing.Union[CallbackQuery, Message]):
    if type(msg) == CallbackQuery:
        msg = msg.message
    user, _ = User.objects.get_or_create(chat_id=msg.chat.id)
    Messages.CarFines.send_if_active(msg.chat.id)
    Dialogs.FINES.next_message(msg.chat.id, index=0, add_markup_buttons=user.build_save_btn(State.BDR))


@bot.message_handler(
    func=lambda msg: msg.from_user.state == 'FINES:Enter_car_series' or (
            msg.from_user.state == 'FINES:Enter_car_number' and SavedSearch.objects.filter(saved_data=msg.text.split(), user__chat_id=msg.chat.id).exists()
    )
)
def fines_document_message(message: Message):
    data = storage.get_user_data(message.chat.id)
    # plate: str = 'АХ8028КЕ', document: str = 'Ррв157324',
    # user_id: int = 1, send = False
    scrap_fines.apply_async(args=[data.get('plate'), message.text, message.chat.id, True])
    Dialogs.FINES.next_message(message.chat.id, index=-1)


@bot.message_handler(func=is_state('FINES:Enter_car_number'))
def fines_car_number(message: Message):
    storage.update_user_data(message.chat.id, 'plate', message.text)
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    Dialogs.FINES.next_message(message.chat.id, add_markup_buttons=user.build_save_btn(State.BDR))


@bot.callback_query_handler(
    func=lambda call: call.data.startswith('bdr#') and User.objects.filter(
        chat_id=call.message.chat.id,
        role='client').exists() is False
)
def fine_subscribe(call: CallbackQuery):
    try:
        markup = call.message.reply_markup
        del markup.keyboard[0]
        bot.edit_message_reply_markup(call.message.chat.id,
                                      call.message.message_id,
                                      reply_markup=markup)
    except Exception as e:
        pass

    try:
        bdr, _ = Bdr.objects.update_or_create(id=call.data.split('#')[-1],
                                              defaults={'status': True}
                                              )
        Messages.FinesSubscribeSuccess.send_if_active(
            call.message.chat.id, format_map={'car_number': bdr.plate}
        )
    except Exception as e:
        logger.debug(f'ERROR FineSubs: {e}')
