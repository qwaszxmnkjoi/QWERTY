from typing import Union

from django.conf import settings
from django.core.paginator import Paginator
from django.utils import timezone
from loguru import logger
from telebot.types import CallbackQuery, Message

from customer.enums import State
from customer.models import (User, Search, DocState, InactiveDocument, Bdr,
                             Departure, Court, Debtors, SavedSearch,
                             Mvs, AsvpElem)
from payment.payment import service
from tbot.messages import Messages
from tbot_messages.bot import bot
from tbot_messages.utils import is_data, is_state


@bot.callback_query_handler(func=is_data('profile_back'))
@bot.message_handler(is_reply_btn_click=Messages.Menu.buttons[5])
@bot.message_handler(
    func=is_state('Assistant'),
    is_reply_btn_click=Messages.Assistant.buttons[0]
)
@bot.message_handler(
    func=is_state('Name:Set'),
    is_reply_btn_click=Messages.Name.buttons[0]
)
@bot.message_handler(
    func=is_state('Name:Set'),
    is_reply_btn_click=Messages.NameNotSet.buttons[0]
)
def cabinet_message(message: Union[Message, CallbackQuery]):
    if type(message) == CallbackQuery:
        message = message.message
    Messages.Profile.send_if_active(message.chat.id, set_state='')


@bot.message_handler(is_reply_btn_click=Messages.Profile.buttons[1])
def assistant_message(message: Message):
    if User.objects.filter(
            chat_id=message.chat.id,
            role='client'
    ).exists():
        try:
            bot_url = 'https://t.me/' + bot.get_me().username
            pay_urls = service.get_pay_links(
                lang=message.from_user.lang,
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
                    'back_callback': 'profile_back'
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

    else:
        Messages.Assistant.send_if_active(message.chat.id,
                                          set_state='Assistant')


@bot.message_handler(is_reply_btn_click=Messages.Profile.buttons[2])
def subscriptions_message(message: Message):
    if User.objects.filter(
            chat_id=message.chat.id,
            role='client'
    ).exists():
        try:
            bot_url = 'https://t.me/' + bot.get_me().username
            pay_urls = service.get_pay_links(
                lang=message.from_user.lang,
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
                    'back_callback': 'profile_back'
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

    else:
        search = Search.objects.filter(user__chat_id=message.chat.id)
        fines = Bdr.objects.filter(user__chat_id=message.chat.id, status=True)
        inactive_doc = InactiveDocument.objects.filter(
            user__chat_id=message.chat.id, subscribe=True)
        doc = DocState.objects.filter(user__chat_id=message.chat.id,
                                      subscribe=True)
        depart = Departure.objects.filter(user__chat_id=message.chat.id,
                                          subscribe=True)
        count = sum(x.count_subs for x in search) + (
                fines.count() + inactive_doc.count() + doc.count() +
                depart.count()
        )

        Messages.MySubscribe.send_if_active(
            message.chat.id, format_map={
                'count': count
            }
        )
        for obj in fines:
            last = obj.bdr_elem.last()
            Messages.FinesSub.send_if_active(
                message.chat.id, format_map={
                    'car_number': obj.plate,
                    'resolution': last.number,
                    'date': last.date.strftime('%d.%m.%Y'),
                    'value': last.amount,
                    'payment': '✅' if last.pay else '❌'
                }, format_keyboard_map={
                    'subs_id': obj.id
                }
            )

        for obj in depart:
            text = ''
            i = 1
            all_days = 0

            for elem in obj.dep_elem.all():
                if elem.date_of_departure is not None:
                    date_of_departure = elem.date_of_departure
                    text += Messages.DepartureTrip.get_text_by_locale(
                        message.chat.id, format_map={
                            'trip': i,
                            'date_of_entry':
                                elem.date_of_entry.strftime('%d/%m/%Y'),
                            'date_of_departure':
                                elem.date_of_departure.strftime('%d/%m/%Y')
                        })
                else:
                    date_of_departure = timezone.now().date()
                    text += Messages.DepartureEntryTrip.get_text_by_locale(
                        message.chat.id, format_map={
                            'trip': i,
                            'date_of_entry':
                                elem.date_of_entry.strftime('%d/%m/%Y'),
                        }
                    )

                all_days += (date_of_departure - elem.date_of_entry).days
                i += 1
            if obj.days < 0:
                text += Messages.DepartViolated.get_text_by_locale(
                    message.chat.id, format_map={'days': -obj.days}
                )
            else:
                text += Messages.DepartLeft.get_text_by_locale(
                    message.chat.id, format_map={'days': obj.days}
                )

            Messages.DepartSub.send_if_active(
                message.chat.id, format_map={'text': text},
                format_keyboard_map={'subs_id': obj.id}
            )

        for obj in doc:
            Messages.DocsSub.send_if_active(
                message.chat.id, format_map={
                    'doc_type': Messages.DocumentsType.get_format_button(
                        button=Messages.DocumentsType.buttons.get(
                            callback_data=obj.type_doc),
                        locale=message.from_user.lang
                    ),
                    'doc_for': Messages.DocumentsId.get_format_button(
                        button=Messages.DocumentsId.buttons.get(
                            callback_data=obj.register_doc),
                        locale=message.from_user.lang
                    ),
                    'number': obj.series if obj.series else '' + obj.number,
                    'status': obj.description
                },
                format_keyboard_map={'subs_id': obj.id}
            )

        for obj in inactive_doc:
            Messages.InactiveSub.send_if_active(
                message.chat.id,
                format_map={
                    'doc_type': Messages.InactiveTypes.get_format_button(
                        button=Messages.InactiveTypes.buttons.get(
                            callback_data=obj.type_doc),
                        locale=message.from_user.lang
                    ),
                    'number': obj.series if obj.series else '' + obj.number,
                    'status': obj.description
                },
                format_keyboard_map={'subs_id': obj.id}
            )

        for obj in search:
            for elem in obj.court.filter(subscribe=True):
                Messages.CourtSub.send_if_active(
                    message.chat.id,
                    format_map={'number': elem.number},
                    format_keyboard_map={'subs_id': elem.id}
                )

            for elem in obj.mvs.filter(subscribe=True):
                Messages.MvsSub.send_if_active(
                    message.chat.id,
                    format_map={'full_name': elem.search.get_full_name},
                    format_keyboard_map={'subs_id': elem.id}
                )

            for asvp in obj.asvp_elem.filter(subscribe=True):
                Messages.AsvpSub.send_if_active(
                    message.chat.id,
                    format_map={'number': asvp.number},
                    format_keyboard_map={'subs_id': asvp.id}
                )


@bot.message_handler(is_reply_btn_click=Messages.Profile.buttons[3])
def name_message(message: Message):
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    if user.name_en:
        Messages.Name.send_if_active(message.chat.id,
                                     format_map={'name_en': str(user.name_en)},
                                     set_state='Name:Set'
                                     )
        bot.send_message(message.chat.id, user.name)
    else:
        Messages.NameNotSet.send_if_active(message.chat.id,
                                           set_state='Name:Set')


@bot.message_handler(func=is_state('Name:Set'))
def set_new_name(message: Message):
    try:
        from transliterate import translit
        name = translit(message.text, 'uk')
        User.objects.update_or_create(chat_id=message.chat.id,
                                      defaults={'name': name,
                                                'name_en': message.text})
        return name_message(message)
    except Exception as e:
        logger.debug(f'ERROR Set Name: {e}')


@bot.message_handler(is_reply_btn_click=Messages.Profile.buttons[4])
def saved_searches(message: Message):
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    if user.role != 'client':
        count_saved = user.saved_search.count()
        Messages.SavedSearch.send_if_active(
            user_id=message.chat.id,
            format_keyboard_map={
                'count': count_saved or None,
                'call_data': 'save_s'
            }
        )
    else:
        try:
            bot_url = 'https://t.me/' + bot.get_me().username
            pay_urls = service.get_pay_links(
                lang=message.from_user.lang,
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
                    'back_callback': 'profile_back'
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


@bot.callback_query_handler(func=lambda call: call.data.startswith('save#'))
def create_saved(call: CallbackQuery):
    data, state_num, obj_id = call.data.split('#')
    state = State.from_num(int(state_num))
    if state == State.BDR:
        bdr = Bdr.objects.get(pk=obj_id)
        saved_data = [bdr.plate, bdr.document]
        user_id = bdr.user_id
    else:
        search = Search.objects.get(pk=obj_id)
        saved_data = search.get_full_name.split()
        user_id = search.user_id

    obj, created = SavedSearch.objects.get_or_create(
        user_id=user_id,
        state=state,
        saved_data=saved_data
    )
    return send_saved(obj, call.from_user.id)


def send_saved(obj: SavedSearch, user_id, page: int = None):
    message_types = {
        State.ASVP.as_str: Messages.SavedAsvp,
        State.BDR.as_str: Messages.SavedBdr,
        State.COURT.as_str: Messages.SavedCourt,
        State.COURT_ASSIGN.as_str: Messages.SavedCourtAssign,
        State.DEBTORS.as_str: Messages.SavedDebtors,
        State.NATIONAL.as_str: Messages.SavedNational,
        State.WANTED.as_str: Messages.SavedWanted

    }
    message: Messages = message_types[obj.state]

    return message.send_if_active(
        user_id,
        format_map={
            'saved_data': obj.data_as_str,
        },
        format_keyboard_map={
            'page': page,
            'obj_id': obj.id
        }
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('save_s'))
def show_saved(call: CallbackQuery):
    try:
        markup = call.message.reply_markup
        del markup.keyboard[0]
        bot.edit_message_reply_markup(call.message.chat.id,
                                      call.message.message_id,
                                      reply_markup=markup)
    except Exception as e:
        pass
    saved_elems = SavedSearch.objects.filter(user__chat_id=call.from_user.id)
    if saved_elems:
        datas = call.data.split('#')
        page = datas[-1] if len(datas) == 2 else 1
        paginator = Paginator(saved_elems, 5)
        page_1 = paginator.page(page)
        objects_list = list(enumerate(page_1.object_list))
        last, _ = objects_list[-1]
        for index, obj in objects_list:
            send_saved(obj, call.from_user.id, page=page_1.next_page_number() if index == last and page_1.has_next() else None)


@bot.callback_query_handler(func=lambda call: call.data.startswith('save_d#'))
def delete_saved(call: CallbackQuery):
    try:
        markup = call.message.reply_markup
        del markup.keyboard[0]
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
    except Exception as e:
        pass

    obj_id = call.data.split('#')[-1]
    saved_elem = SavedSearch.objects.filter(user__chat_id=call.from_user.id, id=obj_id)
    if saved_elem.exists():
        saved_elem.delete()
        Messages.SavedDelete.send_if_active(call.from_user.id, custom_markup=Messages.Profile.get_keyboard_markup(locale=call.from_user.lang))


@bot.message_handler(is_reply_btn_click=Messages.Profile.buttons[5])
def subscribe_user_message(message: Message):
    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    if user.role == 'agent':
        Messages.PaymentAgent.send_if_active(
            user_id=message.chat.id,
            format_keyboard_map={'back_callback': 'profile_back'}
        )
    elif user.role == 'expert':
        if user.subs_id:
            Messages.PaymentAdvanced.send_if_active(
                user_id=message.chat.id,
                format_map={'date_pay': user.date_end.replace(microsecond=0,
                                                              tzinfo=None)},
                format_keyboard_map={'back_callback': 'profile_back'}
            )
        else:
            bot_url = 'https://t.me/' + bot.get_me().username
            pay_urls = service.get_pay_links(
                lang=message.from_user.lang,
                message_id=message.message_id,
                user_id=message.chat.id,
                result_url=bot_url
            )
            data = {
                'liq_url': pay_urls.get('liqpay', bot_url),
                'port_url': pay_urls.get('portmone', bot_url)
            }
            Messages.PaymentReSub.send_if_active(
                user_id=message.chat.id,
                format_map={'date_pay': user.date_end.replace(microsecond=0,
                                                              tzinfo=None)},
                format_keyboard_map={
                    **data,
                    'back_callback': 'profile_back'
                }
            )
    elif user.role == 'client':
        bot_url = 'https://t.me/' + bot.get_me().username
        pay_urls = service.get_pay_links(
            lang=message.from_user.lang,
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
                'back_callback': 'profile_back'
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


@bot.callback_query_handler(func=is_data('cancel_subscribe'))
def cancel_subscribe(call: CallbackQuery):
    user, _ = User.objects.get_or_create(chat_id=call.message.chat.id)
    req = service.cancel_subscribe(user.subs_id)
    if any([x['status'] is True for x in req.values()]):
        user.subs_id = None
        user.save()
        Messages.CancelSubs.send_if_active(
            call.message.chat.id, format_map={
                'date': user.date_end.replace(microsecond=0, tzinfo=None)
            })
    else:
        logger.warning(req['result'])


@bot.callback_query_handler(
    func=lambda call:
    call.data.startswith('bdr_u#') or call.data.startswith('bdr_v#')
)
def subscribe_bdr(call: CallbackQuery):
    if call.data.startswith('bdr_u#'):
        try:
            markup = call.message.reply_markup
            del markup.keyboard[0]
            bot.edit_message_reply_markup(call.message.chat.id,
                                          call.message.message_id,
                                          reply_markup=markup)
        except Exception as e:
            pass
        bdr, _ = Bdr.objects.update_or_create(id=call.data.split('#')[-1],
                                              defaults={'status': False}
                                              )
        Messages.FinesUnSubscribe.send_if_active(
            call.message.chat.id, format_map={'car_number': bdr.plate}
        )
    else:
        bdr, _ = Bdr.objects.get_or_create(id=call.data.split('#')[-1])
        if bdr.bdr_elem:
            for ele in bdr.bdr_elem.all():
                Messages.FinesResult.send_if_active(
                    call.message.chat.id,
                    format_map={'car_number': bdr.plate, 'resolution': ele.number,
                                'date': ele.date.strftime('%d.%m.%Y'),
                                'value': ele.amount,
                                'payment': '✅' if ele.pay else '❌'
                                },
                    format_keyboard_map={'url_view': ele.link},
                    reply_to_message_id=call.message.message_id
                    # custom_markup=None
                )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith('depart_u#')
)
def depart_unsub(call: CallbackQuery):
    Departure.objects.update_or_create(
        id=call.data.split('#')[-1], defaults={'subscribe': False}
    )
    try:
        bot.edit_message_reply_markup(call.message.chat.id,
                                      call.message.message_id,
                                      reply_markup=None)
    except Exception as e:
        pass
    Messages.DepartUnSubs.send_if_active(
        call.message.chat.id, reply_to_message_id=call.message.message_id
    )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith('debt_u#')
)
def debtor_unsub(call: CallbackQuery):
    deb_id = call.data.split('#')[-1]
    debt, created = Debtors.objects.update_or_create(
        id=call.data.split('#')[-1], defaults={'subscribe': False}
    )
    try:
        bot.edit_message_reply_markup(call.message.chat.id,
                                      call.message.message_id,
                                      reply_markup=None)
    except Exception as e:
        pass
    Messages.UnSubscribeDebtors.send_if_active(
        call.message.chat.id, reply_to_message_id=call.message.message_id,
        format_map={'full_name': debt.search.get_full_name},
        format_keyboard_map={'deb_id': deb_id}
    )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith('doc_u#')
)
def doc_unsub(call: CallbackQuery):
    DocState.objects.update_or_create(
        id=call.data.split('#')[-1], defaults={'subscribe': False}
    )
    try:
        bot.edit_message_reply_markup(call.message.chat.id,
                                      call.message.message_id,
                                      reply_markup=None)
    except Exception as e:
        pass
    Messages.DocUnSubs.send_if_active(
        call.message.chat.id, reply_to_message_id=call.message.message_id
    )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith('idoc_u#')
)
def inactive_unsub(call: CallbackQuery):
    InactiveDocument.objects.update_or_create(
        id=call.data.split('doc_u#')[-1], defaults={'subscribe': False}
    )
    try:
        bot.edit_message_reply_markup(call.message.chat.id,
                                      call.message.message_id,
                                      reply_markup=None)
    except Exception as e:
        pass
    Messages.InactiveUnSubs.send_if_active(
        call.message.chat.id, reply_to_message_id=call.message.message_id
    )


@bot.callback_query_handler(
    func=lambda call:
    call.data.startswith('court_u#')
)
def cort_subscribe(call: CallbackQuery):
    if call.data.startswith('court_u#'):
        Court.objects.update_or_create(
            id=call.data.split('#')[-1], defaults={'subscribe': False}
        )
        try:
            markup = call.message.reply_markup
            del markup.keyboard[0]
            bot.edit_message_reply_markup(call.message.chat.id,
                                          call.message.message_id,
                                          reply_markup=markup)
        except Exception as e:
            pass
        Messages.CourtUnSubs.send_if_active(
            call.message.chat.id, reply_to_message_id=call.message.message_id
        )
    else:
        pass


@bot.callback_query_handler(
    func=lambda call:
    call.data.startswith('mvs_u#') or call.data.startswith('mvs_v#')
)
def subscribe_mvs(call: CallbackQuery):
    if call.data.startswith('mvs_u#'):
        Mvs.objects.update_or_create(
            id=call.data.split('#')[-1], defaults={'subscribe': False}
        )
        try:
            markup = call.message.reply_markup
            del markup.keyboard[0]
            bot.edit_message_reply_markup(call.message.chat.id,
                                          call.message.message_id,
                                          reply_markup=markup)
        except Exception as e:
            pass
        Messages.MvsUnSubs.send_if_active(
            call.message.chat.id, reply_to_message_id=call.message.message_id
        )
    else:
        try:
            obj = Mvs.objects.get(id=call.data.split('#')[-1])
            Messages.WantedDetailElem.send_if_active(
                call.message.chat.id,
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
                    'mvs_id': None,
                    'page': None,
                },
                reply_to_message_id=call.message.message_id
            )
        except Mvs.DoesNotExist:
            pass


@bot.callback_query_handler(
    func=lambda call:
    call.data.startswith('asvp_u#') or call.data.startswith('asvp_v#')
)
def subscribe_mvs(call: CallbackQuery):
    if call.data.startswith('asvp_u#'):
        AsvpElem.objects.update_or_create(
            id=call.data.split('#')[-1], defaults={'subscribe': False}
        )
        try:
            markup = call.message.reply_markup
            del markup.keyboard[0]
            bot.edit_message_reply_markup(call.message.chat.id,
                                          call.message.message_id,
                                          reply_markup=markup)
        except Exception as e:
            pass
        Messages.AsvpUnSubs.send_if_active(
            call.message.chat.id, reply_to_message_id=call.message.message_id
        )
    else:
        try:
            obj = AsvpElem.objects.get(id=call.data.split('#')[-1])
            Messages.AsvpDetailElem.send_if_active(
                call.message.chat.id,
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
                    'page': None,
                    'asvp_id': None,
                    'subs_id': None
                },
                reply_to_message_id=call.message.message_id
            )
        except AsvpElem.DoesNotExist:
            pass
