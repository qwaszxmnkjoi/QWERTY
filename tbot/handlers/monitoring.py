from datetime import datetime
from typing import Union

from django.conf import settings
from django.utils import timezone
from loguru import logger
from telebot.types import CallbackQuery, Message

from customer.enums import State
from customer.models import Departure, DepartureElem, Search, Debtors, User
from customer.tasks import national_parsing, scrap_court, scrap_court_assign, scrap_debtors, scrap_asvp, wanted_mws
from payment.payment import service
from tbot.messages import Messages
from tbot.storage import storage
from tbot_messages.bot import bot
from tbot_messages.utils import is_data, is_state


@bot.message_handler(func=is_state('national'),
                     is_reply_btn_click=Messages.StateRegisters.buttons[7])
@bot.callback_query_handler(func=is_data('monitoring_back'))
@bot.message_handler(is_reply_btn_click=Messages.Menu.buttons[0])
@bot.message_handler(is_reply_btn_click=Messages.Enter_car_number.buttons[0],
                     func=is_state('FINES:Enter_car_number'))
@bot.message_handler(is_reply_btn_click=Messages.DepartDate.buttons[0],
                     func=is_state('Depart:DateOfEntry'))
def monitoring(message: Union[Message, CallbackQuery]):
    if type(message) == CallbackQuery:
        message = message.message
    Messages.Monitoring.send_if_active(message.chat.id, set_state='')


@bot.callback_query_handler(
    func=lambda call:
    call.data.startswith('monitoring#') and User.objects.filter(
        chat_id=call.message.chat.id,
        role='client').exists()
)
def unsub_user(call: CallbackQuery):
    try:
        bot_url = 'https://t.me/' + bot.get_me().username
        pay_urls = service.get_pay_links(
            lang=call.from_user.lang,
            message_id=call.message.message_id,
            user_id=call.message.chat.id,
            result_url=bot_url
        )
        data = {
            'liq_url': pay_urls.get('liqpay', bot_url),
            'port_url': pay_urls.get('portmone', bot_url)
        }

        Messages.PayUnsub.send_if_active(
            call.message.chat.id,
            format_map={'cost': service.amount},
            format_keyboard_map={
                **data,
                'back_callback': 'monitoring_back'
            }
        )
        try:
            lang = call.message.from_user.lang or 'ru'
            with open(settings.MEDIA_ROOT / f'опис_{lang}.docx', 'rb') as detail_file:
                Messages.PayUnsub.send_if_active(
                    user_id=call.message.chat.id,
                    file=detail_file,
                    custom_text=''
                )
        except Exception as e:
            logger.debug(e)
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=is_data('monitoring#depart'))
@bot.callback_query_handler(
    func=lambda call:
    call.data == 'back' and call.from_user.state == 'Depart:DateOfDeparture'
)
@bot.callback_query_handler(
    func=lambda call:
    call.data == 'back' and call.from_user.state == 'Depart:Calculate'
)
@bot.callback_query_handler(
    func=lambda call:
    call.data == 'add_trip' and call.from_user.state == 'Depart:Calculate'
)
def depart_message(call: CallbackQuery):
    logger.debug('depart_message')
    logger.debug(call.from_user.state)
    storage.set_user_state(call.message.chat.id, 'Depart:DateOfEntry')
    if call.data == 'add_trip':
        data = storage.get_user_data(call.message.chat.id)
        storage.set_user_data(call.message.chat.id,
                              {'locale': call.from_user.lang,
                               'depart_id': data.get('depart_id', None)}
                              )
    else:
        storage.set_user_data(call.message.chat.id,
                              {'locale': call.from_user.lang}
                              )
        Messages.DepartTerm.send_if_active(call.message.chat.id)
    Messages.DepartDate.send_if_active(call.message.chat.id)


@bot.message_handler(func=is_state('Depart:DateOfEntry'))
def depart_entry_message(message: Message):
    try:
        data = storage.get_user_data(message.chat.id)
        if data.get('date_of_entry'):
            date_of_entry = data['date_of_entry']
        else:
            date_of_entry = message.text
            datetime.strptime(date_of_entry, '%d/%m/%Y')
            storage.update_user_data(message.chat.id, 'date_of_entry',
                                     date_of_entry)
        if data.get('depart_id') is not None:
            depart_elems = DepartureElem.objects.filter(
                departure_id=data['depart_id']
            )
            count = depart_elems.count() + 1
        else:
            count = 1

        storage.update_user_data(message.chat.id, 'count', count)

        Messages.DepartDateEntry.send_if_active(
            message.chat.id, format_map={
                'depart_num': count,
                'date_of_entry': date_of_entry
            },
            set_state='Depart:DateOfDeparture'
        )
    except Exception as e:
        logger.debug(f'Depart DateOfEntry: {e}')
        Messages.DepartDate.send_if_active(message.chat.id)


@bot.callback_query_handler(
    func=lambda call: call.data == 'no_departure' and is_state(
        'Depart:DateOfDeparture')
)
def depart_skip_departure_date(call: CallbackQuery):
    call.message.from_user = call.from_user
    return depart_departure_message(call.message, no_depart=True)


@bot.message_handler(func=is_state('Depart:DateOfDeparture'))
def depart_departure_message(message: Message, no_depart: bool = False):
    data = storage.get_user_data(message.chat.id)
    try:
        storage.set_user_state(message.chat.id, 'Depart:Calculate')
        if no_depart is False:
            date_of_departure = datetime.strptime(message.text, '%d/%m/%Y')
            storage.update_user_data(message.chat.id, 'date_of_departure',
                                     message.text)
        else:
            date_of_departure = datetime.strptime(
                timezone.now().strftime('%d/%m/%Y'), '%d/%m/%Y')

        date_of_entry = datetime.strptime(data.get('date_of_entry'),
                                          '%d/%m/%Y')
        days_left = data.get('days_left', 90)

        if (date_of_departure - date_of_entry).days < 0:
            Messages.DepartDateError.send_if_active(
                message.chat.id,
                custom_markup=Messages.Menu.get_keyboard_markup(
                    data.get('locale')
                )
            )
            return

        if data.get('depart_id') is not None:
            dep = Departure.objects.get(id=data['depart_id'])
        else:
            user, _ = User.objects.get_or_create(chat_id=message.chat.id)
            dep = Departure.objects.create(user=user)
            storage.update_user_data(message.chat.id, 'depart_id', dep.id)

        if no_depart:
            DepartureElem.objects.get_or_create(
                departure_id=dep.id, date_of_entry=date_of_entry
            )
        else:
            DepartureElem.objects.get_or_create(
                departure_id=dep.id, date_of_entry=date_of_entry,
                date_of_departure=date_of_departure
            )

        dep_elements = DepartureElem.objects.filter(departure_id=dep.id)

        i = 1
        all_days = 0
        text = ''

        for element in dep_elements:
            if element.date_of_departure is not None:
                date_of_departure = element.date_of_departure
                text += Messages.DepartureTrip.get_text_by_locale(
                    message.chat.id, format_map={
                        'trip': i,
                        'date_of_entry':
                            element.date_of_entry.strftime('%d/%m/%Y'),
                        'date_of_departure':
                            element.date_of_departure.strftime('%d/%m/%Y')
                    })
            else:
                date_of_departure = timezone.now().date()
                text += Messages.DepartureEntryTrip.get_text_by_locale(
                    message.chat.id, format_map={
                        'trip': i,
                        'date_of_entry':
                            element.date_of_entry.strftime('%d/%m/%Y'),
                    }
                )

            all_days += (date_of_departure - element.date_of_entry).days
            i += 1

        result = days_left - all_days
        dep.days = result
        dep.save()

        if result < 0:
            text += Messages.DepartViolated.get_text_by_locale(
                message.chat.id, format_map={'days': -result}
            )
        else:
            text += Messages.DepartLeft.get_text_by_locale(
                message.chat.id, format_map={'days': result}
            )

        if dep_elements.last().date_of_departure is not None:
            bot.send_message(
                message.chat.id, text,
                reply_markup=Messages.DepartureTrip.get_keyboard_markup(
                    data.get('locale')))
        else:
            bot.send_message(
                message.chat.id, text,
                reply_markup=Messages.DepartureEntryTrip.get_keyboard_markup(
                    data.get('locale')))

    except Exception as e:
        logger.debug(f'Depart DateOfDeparture: {e}')
        try:
            bot.delete_message(message.chat.id, message.message_id - 1)
            bot.delete_message(message.chat.id, message.message_id)
        except Exception:
            pass
        Messages.DepartDateEntry.send_if_active(
            message.chat.id, format_map={
                'depart_num': data.get('count', 1),
                'date_of_entry': data.get('date_of_entry')
            }
        )


@bot.callback_query_handler(
    func=lambda call:
    call.data == 'subscribe' and call.from_user.state == 'Depart:Calculate'
)
def subscribe_depart(call: CallbackQuery):
    data = storage.get_user_data(call.message.chat.id)
    Departure.objects.update_or_create(id=data.get('depart_id'),
                                       defaults={'subscribe': True})
    storage.set_user_data(
        call.message.chat.id, {'locale': call.from_user.lang}
    )
    storage.set_user_state(call.message.chat.id)
    Messages.DepartSubs.send_if_active(
        call.message.chat.id, custom_markup=Messages.Menu.get_keyboard_markup(
            call.from_user.lang
        )
    )


@bot.callback_query_handler(func=is_data('monitoring#state'))
def monitoring_national(call: CallbackQuery):
    Messages.StateRegisters.send_if_active(call.message.chat.id, set_state='national')


@bot.message_handler(func=is_state('national'),
                     is_reply_btn_click=Messages.StateRegisters.buttons[1])
def about_national(message: Message):
    Messages.AboutStateRegisters.send_if_active(message.chat.id, set_state='about_national')


@bot.callback_query_handler(func=is_data('national_search'))
@bot.message_handler(func=is_state('national'),
                     is_reply_btn_click=Messages.StateRegisters.buttons[0])
def national_search(msg: Union[Message, CallbackQuery]):
    if type(msg) == CallbackQuery:
        msg.message.from_user = msg.from_user
        msg = msg.message
    user, _ = User.objects.get_or_create(chat_id=msg.chat.id)
    Messages.MonitoringNational.send_if_active(
        user_id=msg.chat.id,
        format_keyboard_map={'name': None if user.name is None or user.name == '' else user.name},
        add_markup_buttons=user.build_save_btn(State.NATIONAL.as_str),
        set_state='monitoring_name'
    )


@bot.message_handler(
    func=lambda message: message.from_user.state == 'monitoring_name' and (
            Messages.MonitoringNational.get_format_button(
                index=0,
                locale=message.from_user.lang,
                format_map={
                    'name': User.objects.get_or_create(
                        chat_id=message.chat.id
                    )[0].name
                }
            ) == message.text or (len(message.text.split(' ')) == 2 or len(message.text.split(' ')) == 3)
    )
)
def start_monitoring(message: Message):
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    if user.role != 'client':
        is_saved = Messages.MonitoringNational.get_format_button(
            index=0,
            locale=message.from_user.lang,
            format_map={'name': user.name}
        ) == message.text
        if is_saved:
            name = user.name.split(' ')
        else:
            name = message.text.split(' ')
        search = Search.objects.create(
            user=user, name=name[1], surname=name[0],
            patronymic=None if len(name) == 2 else name[2],
            status=False
        )
        national_parsing.apply_async(
            args=[search.id, True, message.message_id]
        )
    storage.set_user_state(message.chat.id, '')


@bot.callback_query_handler(func=is_data('court_search'))
@bot.message_handler(func=is_state('national'),
                     is_reply_btn_click=Messages.StateRegisters.buttons[2])
def court_search(msg: Union[Message, CallbackQuery]):
    if type(msg) == CallbackQuery:
        msg.message.from_user = msg.from_user
        msg = msg.message
    user, _ = User.objects.get_or_create(chat_id=msg.chat.id)
    Messages.MonitoringNational.send_if_active(
        user_id=msg.chat.id,
        format_keyboard_map={'name': None}, add_markup_buttons=user.build_save_btn(State.COURT),
        set_state='court_name'
    )


@bot.message_handler(
    func=lambda message: message.from_user.state == 'court_name' and (len(message.text.split(' ')) == 2 or len(message.text.split(' ')) == 3)
)
def start_monitoring_court(message: Message):
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    if user.role != 'client':
        name = message.text.split(' ')
        search = Search.objects.create(
            user=user, name=name[1], surname=name[0],
            patronymic=None if len(name) == 2 else name[2],
            status=False
        )
        scrap_court.apply_async(
            args=[search.id, True, message.message_id]
        )
    storage.set_user_state(message.chat.id, '')


@bot.callback_query_handler(func=is_data('assign_search'))
@bot.message_handler(func=is_state('national'),
                     is_reply_btn_click=Messages.StateRegisters.buttons[3])
def court_search(msg: Union[Message, CallbackQuery]):
    if type(msg) == CallbackQuery:
        msg.message.from_user = msg.from_user
        msg = msg.message
    user, _ = User.objects.get_or_create(chat_id=msg.chat.id)
    Messages.MonitoringNational.send_if_active(
        user_id=msg.chat.id,
        format_keyboard_map={'name': None}, add_markup_buttons=user.build_save_btn(State.COURT_ASSIGN),
        set_state='assign_name'
    )


@bot.message_handler(
    func=lambda message: message.from_user.state == 'assign_name' and (len(message.text.split(' ')) == 2 or len(message.text.split(' ')) == 3)
)
def start_monitoring_court_assign(message: Message):
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    if user.role != 'client':
        name = message.text.split(' ')
        search = Search.objects.create(
            user=user, name=name[1], surname=name[0],
            patronymic=None if len(name) == 2 else name[2],
            status=False
        )
        scrap_court_assign.apply_async(
            args=[search.id, True, message.message_id]
        )
    storage.set_user_state(message.chat.id, '')


@bot.callback_query_handler(func=is_data('debtors_search'))
@bot.message_handler(func=is_state('national'), is_reply_btn_click=Messages.StateRegisters.buttons[4])
def deb_search(msg: Union[Message, CallbackQuery]):
    if type(msg) == CallbackQuery:
        msg.message.from_user = msg.from_user
        msg = msg.message
    user, _ = User.objects.get_or_create(chat_id=msg.chat.id)
    Messages.MonitoringNational.send_if_active(
        user_id=msg.chat.id,
        format_keyboard_map={'name': None}, add_markup_buttons=user.build_save_btn(State.DEBTORS),
        set_state='debtors_name'
    )


@bot.message_handler(
    func=lambda message: message.from_user.state == 'debtors_name' and (len(message.text.split(' ')) == 2 or len(message.text.split(' ')) == 3)
)
def start_monitoring_debtors(message: Message):
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    if user.role != 'client':
        name = message.text.split(' ')
        search = Search.objects.create(
            user=user, name=name[1], surname=name[0],
            patronymic=None if len(name) == 2 else name[2],
            status=False
        )
        debt, add = Debtors.objects.get_or_create(search=search)
        scrap_debtors.apply_async(
            args=[debt.id, True, message.message_id]
        )
    storage.set_user_state(message.chat.id, '')


@bot.callback_query_handler(func=is_data('asvp_search'))
@bot.message_handler(func=is_state('national'), is_reply_btn_click=Messages.StateRegisters.buttons[5])
def asvp_search(msg: Union[Message, CallbackQuery]):
    if type(msg) == CallbackQuery:
        msg.message.from_user = msg.from_user
        msg = msg.message
    user, _ = User.objects.get_or_create(chat_id=msg.chat.id)
    Messages.MonitoringNational.send_if_active(
        user_id=msg.chat.id,
        format_keyboard_map={'name': None}, add_markup_buttons=user.build_save_btn(State.ASVP),
        set_state='asvp_name'
    )


@bot.message_handler(
    func=lambda message: message.from_user.state == 'asvp_name' and (len(message.text.split(' ')) == 2 or len(message.text.split(' ')) == 3)
)
def start_monitoring_asvp(message: Message):
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    if user.role != 'client':
        name = message.text.split(' ')
        search = Search.objects.create(
            user=user, name=name[1], surname=name[0],
            patronymic=None if len(name) == 2 else name[2],
            status=False
        )
        scrap_asvp.apply_async(
            args=[search.id, True, message.message_id]
        )
    storage.set_user_state(message.chat.id, '')


@bot.callback_query_handler(func=is_data('wanted_search'))
@bot.message_handler(func=is_state('national'), is_reply_btn_click=Messages.StateRegisters.buttons[6])
def wanted_search(msg: Union[Message, CallbackQuery]):
    if type(msg) == CallbackQuery:
        msg.message.from_user = msg.from_user
        msg = msg.message
    user, _ = User.objects.get_or_create(chat_id=msg.chat.id)
    Messages.MonitoringNational.send_if_active(
        user_id=msg.chat.id,
        format_keyboard_map={'name': None}, add_markup_buttons=user.build_save_btn(State.WANTED),
        set_state='wanted_name'
    )


@bot.message_handler(
    func=lambda message: message.from_user.state == 'wanted_name' and (len(message.text.split(' ')) == 2 or len(message.text.split(' ')) == 3)
)
def start_monitoring_wanted(message: Message):
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    if user.role != 'client':
        name = message.text.split(' ')
        search = Search.objects.create(
            user=user, name=name[1], surname=name[0],
            patronymic=None if len(name) == 2 else name[2],
            status=False
        )
        wanted_mws.apply_async(
            args=[search.id, True, message.message_id]
        )
    storage.set_user_state(message.chat.id, '')


@bot.message_handler(commands=['detail_court'],
                     func=lambda message: User.objects.filter(
                         chat_id=message.chat.id,
                         role='client').exists() is False
                     )
def court_detail(message: Message):
    Messages.CourtDetail.send_if_active(message.chat.id)


@bot.message_handler(commands=['detail_court_assign'],
                     func=lambda message: User.objects.filter(
                         chat_id=message.chat.id,
                         role='client').exists() is False
                     )
def court_assign_detail(message: Message):
    Messages.AssignDetail.send_if_active(message.chat.id)


@bot.message_handler(commands=['detail_debtors'],
                     func=lambda message: User.objects.filter(
                         chat_id=message.chat.id,
                         role='client').exists() is False
                     )
def debtors_detail(message: Message):
    Messages.DebtorsDetail.send_if_active(message.chat.id)


@bot.message_handler(commands=['detail_asvp'],
                     func=lambda message: User.objects.filter(
                         chat_id=message.chat.id,
                         role='client').exists() is False
                     )
def asvp_detail(message: Message):
    Messages.AsvpDetail.send_if_active(message.chat.id)


@bot.message_handler(commands=['detail_wanted'],
                     func=lambda message: User.objects.filter(
                         chat_id=message.chat.id,
                         role='client').exists() is False
                     )
def wanted_detail(message: Message):
    Messages.WantedDetail.send_if_active(message.chat.id)
