from django.conf import settings
from django.core.paginator import Paginator
from django.utils.formats import localize
from loguru import logger
from telebot.types import CallbackQuery, Message

from customer.models import (AsvpElem, Court, CourtAssignment, Debtors, Mvs, Search, User)
from payment.payment import service
from tbot.messages import Messages
from tbot.storage import storage
from tbot_messages.bot import bot
from tbot_messages.utils import is_state


@bot.message_handler(regexp='court_|court_assign_|wanted_|debtors_|asvp_([0-9]*)',
                     func=lambda message: User.objects.filter(chat_id=message.chat.id, role='client').exists()
                     )
def unsub_subscribe(message: Message):
    try:
        bot_url = 'https://t.me/' + bot.get_me().username
        pay_urls = service.get_pay_links(
            lang=getattr(message.from_user, 'lang', 'en'),
            message_id=message.message_id,
            user_id=message.chat.id,
            result_url=bot_url
        )
        data = {
            'liq_url': pay_urls.get('liqpay', bot_url),
            'port_url': pay_urls.get('portmone', bot_url)
        }

        Messages.PayUnsub.send_if_active(
            message.chat.id,
            format_map={'cost': service.amount},
            format_keyboard_map={
                **data,
                'back_callback': 'menu'
            }
        )
        try:
            lang = message.from_user.lang or 'ru'
            with open(settings.MEDIA_ROOT / f'опис_{lang}.docx', 'rb') as detail_file:
                Messages.PayUnsub.send_if_active(
                    user_id=message.chat.id,
                    file=detail_file,
                    custom_text='',
                    custom_markup=None
                )
        except Exception as e:
            logger.debug(e)
    except Exception as e:
        logger.error(e)


@bot.message_handler(regexp='court_assign_([0-9]*)')
def court_assign_result(message: Message, page: int = 1, is_show_detail: bool = True):
    if page == 1 and is_show_detail:
        assign_id = message.text.split('_')[-1]
    else:
        assign_id = storage.get_user_data(message.chat.id).get('assign_id', 0)
    try:
        assign = CourtAssignment.objects.get(id=assign_id)
        assign_elems = assign.assign_elem.all()
        if count := len(assign_elems):
            full_name = assign.search.get_full_name
            if page == 1 and is_show_detail:
                Messages.CourtAssignSearch.send_if_active(
                    message.chat.id,
                    format_map={
                        'full_name': full_name,
                        'count': count
                    },
                    format_keyboard_map={
                        'show_call': None,
                        'id_sub': assign.id if assign.subscribe else None,
                    },
                    set_state='assign_view',
                )
                storage.update_user_data(message.chat.id, 'assign_id', assign_id)
            paginator = Paginator(assign_elems, 5)
            page_1 = paginator.page(page)
            objects_list = list(enumerate(page_1.object_list))
            last, _ = objects_list[-1]
            for index, obj in objects_list:
                Messages.CourtAssignDetail.send_if_active(
                    message.chat.id,
                    format_map={
                        'dt_meet': localize(obj.dt_meet),
                        'judges': obj.judges.replace(full_name, f'<b><i>{full_name}</i></b>'),
                        'number': obj.number,
                        'name_court': obj.name_court,
                        'room_court': obj.room_court,
                        'involved': obj.involved.replace(full_name, f'<b><i>{full_name}</i></b>'),
                        'description': obj.description.replace(full_name, f'<b><i>{full_name}</i></b>'),
                        'address': obj.address,
                    },
                    format_keyboard_map={
                        'page': page_1.next_page_number() if index == last and page_1.has_next() else None
                    }
                )
    except CourtAssignment.DoesNotExist:
        logger.debug(f'CourtAssignment with id {assign_id} DoesNotExist')


@bot.message_handler(regexp='court_([0-9]*)')
def court_result(message: Message, page: int = 1, is_show_detail: bool = True):
    if page == 1 and is_show_detail:
        search_id = message.text.split('_')[-1]
    else:
        search_id = storage.get_user_data(message.chat.id).get('search_id', 0)
    try:
        search = Search.objects.get(id=search_id)
        if search.court:
            if page == 1 and is_show_detail:
                Messages.CourtDetailSearch.send_if_active(
                    message.chat.id,
                    format_map={
                        'full_name': search.get_full_name,
                        'count': search.court.count()
                    },
                    custom_markup=None,
                    set_state='court_view',
                )
                storage.update_user_data(message.chat.id, 'search_id', search_id)
            paginator = Paginator(search.court.all(), 5)
            page_1 = paginator.page(page)
            objects_list = list(enumerate(page_1.object_list))
            last, _ = objects_list[-1]
            for index, obj in objects_list:
                Messages.CourtDetailElem.send_if_active(
                    message.chat.id,
                    format_map={
                        'court': obj.court,
                        'number': obj.number,
                        'form': obj.form,
                        'claimant': obj.claimant,
                    },
                    format_keyboard_map={
                        'court_id': obj.id if obj.court_elem.count() else None,
                        'court_sub': obj.id if obj.subscribe is False else None,
                        'page': page_1.next_page_number() if index == last and page_1.has_next() else None
                    }
                )
    except Search.DoesNotExist:
        logger.debug(f'Search with id {search_id} DoesNotExist')


def detail_court_info(message: Message, court_id: int):

    try:
        court = Court.objects.get(id=court_id)
        if court.court_elem.count():
            for obj in court.court_elem.all():
                Messages.CourtResultDetail.send_if_active(
                    message.chat.id,
                    format_map={
                        'date_approval': obj.date_approval,
                        'number': obj.number,
                        'chairmen': obj.chairmen,
                        'form': obj.form,
                        'court_type': obj.court_type,
                    },
                    format_keyboard_map={
                        'link': obj.link
                    },
                    reply_to_message_id=message.message_id
                )
    except Court.DoesNotExist:
        logger.debug(f'Court with id {court_id} DoesNotExist')


@bot.callback_query_handler(
    func=lambda call:
    call.data.startswith('court_v#')
)
def court_v(call: CallbackQuery):
    call.message.from_user = call.from_user
    msg = call.message
    return detail_court_info(msg, int(call.data.split("#")[-1]))


@bot.callback_query_handler(func=is_state('court_view'))
def court_view(call: CallbackQuery):
    call.message.from_user = call.from_user
    msg = call.message
    if call.data == 'show_result':
        return court_result(call.message, is_show_detail=False)
    elif call.data.startswith('v#'):
        return detail_court_info(msg, int(call.data.split("#")[-1]))
    elif call.data.startswith('next#'):
        markup = msg.reply_markup
        del markup.keyboard[-1]
        try:
            bot.edit_message_reply_markup(chat_id=msg.chat.id,
                                          message_id=msg.message_id,
                                          reply_markup=markup)
        except Exception as e:
            logger.debug(f'ERROR edit markup: {e}')
        return court_result(msg, int(call.data.split("#")[-1]))
    elif call.data.startswith('subs#'):
        try:
            markup = msg.reply_markup
            if len(markup.keyboard) == 1:
                del markup.keyboard[0]
            else:
                del markup.keyboard[1]
            court = Court.objects.get(id=call.data.split('#')[-1])
            bot.edit_message_reply_markup(msg.chat.id, msg.message_id, reply_markup=markup)
            court.subscribe = True
            court.save()
            Messages.SubscribeCourt.send_if_active(
                msg.chat.id, reply_to_message_id=msg.message_id
            )
        except Court.DoesNotExist:
            logger.debug(f'Court with id {call.data.split("#")[-1]}'
                         f' DoesNotExist')


@bot.callback_query_handler(func=is_state('assign_view'))
def assign_view(call: CallbackQuery):
    call.message.from_user = call.from_user
    msg = call.message
    if call.data == 'show_result':
        return court_assign_result(call.message, is_show_detail=False)
    elif call.data.startswith('subs#'):
        try:
            assign = CourtAssignment.objects.get(id=call.data.split('#')[-1])
            bot.edit_message_reply_markup(msg.chat.id, msg.message_id, reply_markup=None)
            assign.subscribe = True
            assign.save()
            Messages.CourtAssignSubscribe.send_if_active(
                msg.chat.id, reply_to_message_id=msg.message_id
            )
        except Court.DoesNotExist:
            logger.debug(f'Court with id {call.data.split("#")[-1]}'
                         f' DoesNotExist')

    elif call.data.startswith('next#'):
        markup = msg.reply_markup
        del markup.keyboard[-1]
        try:
            bot.edit_message_reply_markup(chat_id=msg.chat.id,
                                          message_id=msg.message_id,
                                          reply_markup=markup)
        except Exception as e:
            logger.debug(f'ERROR edit markup: {e}')
        return court_assign_result(msg, int(call.data.split('#')[-1]))


@bot.message_handler(regexp='wanted_([0-9]*)')
def wanted_result(message: Message, page: int = 1, is_show_detail: bool = True):
    if page == 1 and is_show_detail:
        search_id = message.text.split('_')[-1]
    else:
        search_id = storage.get_user_data(message.chat.id).get('search_id', 0)
    try:
        search = Search.objects.get(id=search_id)
        wanted = search.mvs.all()
        if len(wanted):
            if page == 1 and is_show_detail:
                Messages.WantedDetailSearch.send_if_active(
                    message.chat.id,
                    format_map={
                        'full_name': search.get_full_name,
                        'count': len(wanted)
                    },
                    format_keyboard_map={'show_data': None},
                    add_user_data={'search_id': search_id},
                    set_state='wanted_view',
                )
            paginator = Paginator(wanted, 5)
            page_1 = paginator.page(page)
            objects_list = list(enumerate(page_1.object_list))
            last, _ = objects_list[-1]
            for index, obj in objects_list:
                Messages.WantedDetailElem.send_if_active(
                    message.chat.id,
                    format_map={
                        'region': obj.region,
                        'category': obj.category if obj.category else '-',
                        'disappearance': obj.disappearance
                        if obj.disappearance else '-',
                        'accusations': obj.accusations
                        if obj.accusations else '-',
                        'birth': obj.birth if obj.birth else '-',
                        'precaution': obj.precaution
                        if obj.precaution else '-',
                    },
                    format_keyboard_map={
                        'link': obj.link,
                        'mvs_id': obj.id if obj.subscribe is False else None,
                        'page': page_1.next_page_number()
                        if index == last and page_1.has_next() else None,
                    }
                )
    except Search.DoesNotExist:
        logger.debug(f'Search with id {search_id} DoesNotExist')


@bot.callback_query_handler(func=is_state('wanted_view'))
def wanted_view(call: CallbackQuery):
    call.message.from_user = call.from_user
    msg = call.message
    if call.data == 'show_result':
        return wanted_result(call.message, is_show_detail=False)
    elif call.data.startswith('next#'):
        markup = msg.reply_markup
        del markup.keyboard[-1]
        try:
            bot.edit_message_reply_markup(chat_id=msg.chat.id,
                                          message_id=msg.message_id,
                                          reply_markup=markup)
        except Exception as e:
            logger.debug(f'ERROR edit markup: {e}')
        return wanted_result(msg, int(call.data.split("#")[-1]))
    elif call.data.startswith('subs#'):
        try:
            markup = msg.reply_markup
            del markup.keyboard[1]
            mvs = Mvs.objects.get(id=call.data.split('#')[-1])
            bot.edit_message_reply_markup(msg.chat.id, msg.message_id,
                                          reply_markup=markup)
            mvs.subscribe = True
            mvs.save()
            Messages.SubscribeWanted.send_if_active(
                msg.chat.id, reply_to_message_id=msg.message_id
            )
        except Mvs.DoesNotExist:
            logger.debug(f'Mvs with id {call.data.split("#")[-1]}'
                         f' DoesNotExist')


@bot.message_handler(regexp='debtors_([0-9]*)')
def debtors_result(message: Message, page: int = 1, is_show_detail: bool = True):
    if page == 1 and is_show_detail:
        debtors_id = message.text.split('_')[-1]
    else:
        debtors_id = storage.get_user_data(message.chat.id).get('debtors_id', 0)
    try:
        debtors = Debtors.objects.get(id=debtors_id)
        deb_elems = debtors.debtors_elem.all()
        if len(deb_elems):
            if page == 1 and is_show_detail:
                Messages.DebtorsDetailSearch.send_if_active(
                    message.chat.id,
                    format_map={
                        'full_name': debtors.search.get_full_name,
                        'count': len(deb_elems)
                    },
                    format_keyboard_map={'show_data': None, 'deb_id': debtors_id if not debtors.subscribe else None, 'subs_id': debtors_id if debtors.subscribe else None},
                    add_user_data={'debtors_id': debtors_id},
                    set_state='debtors_view',
                )
            paginator = Paginator(deb_elems, 5)
            page_1 = paginator.page(page)
            objects_list = list(enumerate(page_1.object_list))
            last, _ = objects_list[-1]
            for index, obj in objects_list:
                Messages.DebtorsDetailElem.send_if_active(
                    message.chat.id,
                    format_map={
                        'birth': obj.birth,
                        'publisher': obj.publisher if obj.publisher else '-',
                        'connection': obj.connection
                        if obj.connection else '-',
                        'number': obj.number
                        if obj.number else '-',
                        'deduction': obj.deduction if obj.deduction else '-',
                    },
                    format_keyboard_map={
                        'page': page_1.next_page_number()
                        if index == last and page_1.has_next() else None,
                    }
                )
    except Debtors.DoesNotExist:
        logger.debug(f'Debtors with id {debtors_id} DoesNotExist')


@bot.callback_query_handler(func=is_state('debtors_view'))
def debtors_view(call: CallbackQuery):
    call.message.from_user = call.from_user
    msg = call.message
    deb_id = call.data.split("#")[-1]
    if call.data == 'show_result':
        return debtors_result(msg, is_show_detail=False)
    elif call.data.startswith('next#'):
        try:
            bot.edit_message_reply_markup(chat_id=msg.chat.id,
                                          message_id=msg.message_id,
                                          reply_markup=None)
        except Exception as e:
            logger.debug(f'ERROR edit markup: {e}')
        return debtors_result(msg, int(deb_id))
    elif call.data.startswith('subs#'):
        try:
            markup = msg.reply_markup
            del markup.keyboard[-1]
            debt = Debtors.objects.get(id=deb_id)
            bot.edit_message_reply_markup(msg.chat.id, msg.message_id, reply_markup=markup)
            debt.subscribe = True
            debt.save()
            Messages.SubscribeDebtors.send_if_active(
                msg.chat.id, reply_to_message_id=msg.message_id
            )
        except Debtors.DoesNotExist:
            logger.debug(f'Debtors with id {deb_id} DoesNotExist')


@bot.message_handler(regexp='asvp_([0-9]*)')
def asvp_result(message: Message, page: int = 1, is_show_detail: bool = True):
    if page == 1 and is_show_detail:
        search_id = message.text.split('_')[-1]
    else:
        search_id = storage.get_user_data(message.chat.id).get('search_id', 0)
    try:
        search = Search.objects.get(id=search_id)
        asvp_elems = search.asvp_elem.all()
        if len(asvp_elems):
            if page == 1 and is_show_detail:
                Messages.AsvpDetailSearch.send_if_active(
                    message.chat.id,
                    format_map={
                        'full_name': search.get_full_name,
                        'count': len(asvp_elems)
                    },
                    format_keyboard_map={'show_data': None},
                    add_user_data={'search_id': search_id},
                    set_state='asvp_view',
                )
            paginator = Paginator(asvp_elems, 5)
            page_1 = paginator.page(page)
            objects_list = list(enumerate(page_1.object_list))
            last, _ = objects_list[-1]
            for index, obj in objects_list:
                Messages.AsvpDetailElem.send_if_active(
                    message.chat.id,
                    format_map={
                        'creditors_name': obj.creditors_name if obj.creditors_name else '-',
                        'agency': obj.agency if obj.agency else '-',
                        'date_open': obj.date_open if obj.date_open else '-',
                        'birth': obj.birth if obj.birth else '-',
                        'debtors': obj.debtors if obj.debtors else '-',
                        'number': obj.number if obj.number else '-',
                        'status': obj.status
                    },
                    format_keyboard_map={
                        'page': page_1.next_page_number()
                        if index == last and page_1.has_next() else None,
                        'asvp_id': obj.id if obj.subscribe is False else None,
                        'subs_id': obj.id if obj.subscribe else None
                    }
                )
    except Debtors.DoesNotExist:
        logger.debug(f'Search with id {search_id} DoesNotExist')


@bot.callback_query_handler(func=is_state('asvp_view'))
def asvp_view(call: CallbackQuery):
    call.message.from_user = call.from_user
    msg = call.message
    if call.data == 'show_result':
        return asvp_result(msg, is_show_detail=False)
    elif call.data.startswith('next#'):
        markup = msg.reply_markup
        del markup.keyboard[-1]
        try:
            bot.edit_message_reply_markup(chat_id=msg.chat.id,
                                          message_id=msg.message_id,
                                          reply_markup=markup)
        except Exception as e:
            logger.debug(f'ERROR edit markup: {e}')
        return asvp_result(msg, int(call.data.split("#")[-1]))
    elif call.data.startswith('subs#'):
        try:
            markup = msg.reply_markup
            del markup.keyboard[0]
            asvp = AsvpElem.objects.get(id=call.data.split('#')[-1])
            bot.edit_message_reply_markup(msg.chat.id, msg.message_id,
                                          reply_markup=markup)
            asvp.subscribe = True
            asvp.save()
            Messages.SubscribeAsvp.send_if_active(
                msg.chat.id, reply_to_message_id=msg.message_id
            )
        except Mvs.DoesNotExist:
            logger.debug(f'AsvpElem with id {call.data.split("#")[-1]}'
                         f' DoesNotExist')

