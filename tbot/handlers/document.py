from datetime import datetime
from typing import Union

from django.contrib.postgres.search import SearchVector
from django.utils import timezone
from loguru import logger
from telebot.types import CallbackQuery, Message

from customer.models import DocState, InactiveDocument, User
from customer.tasks import doc_state, inactive_doc
from tbot.messages import Dialogs, Messages
from tbot.storage import storage
from tbot_messages.bot import bot
from tbot_messages.utils import (generate_inline_result_from_queryset, is_data,
                                 is_state)


@bot.callback_query_handler(func=is_data('monitoring#docstate'))
@bot.callback_query_handler(
    func=lambda call:
    call.data == 'back' and call.from_user.state == 'DOCUMENTS:ChoiceKind'
)
def docs_message(msg: Union[CallbackQuery, Message]):
    if type(msg) == CallbackQuery:
        msg = msg.message
        storage.update_user_data(msg.chat.id, 'document', None)
    Messages.DocumentsReadiness.send_if_active(msg.chat.id,
                                               set_state='DOCUMENTS:Select')


@bot.inline_handler(func=is_state('DOCUMENTS:Select'))
def docs_list(query):
    docs = Messages.DocumentsType.buttons
    locale = query.from_user.lang

    if query.query:
        if locale:
            docs = docs.annotate(
                search=SearchVector('text', f'text_{locale}'),
            ).filter(search__icontains=query.query)
        else:
            docs = docs.filter(text__icontains=query.query)

    inlines = generate_inline_result_from_queryset(
        query_set=docs,
        offset=int(query.offset) if query.offset else 0,
        title=f'text_{locale}' if locale else 'text',
        title_attr=True,
        description=None,
        id_attr='callback_data',
        text=f'text_{locale}' if locale else 'text',
        text_attr=True
    )

    bot.answer_inline_query(
        inline_query_id=query.id,
        results=inlines,
        cache_time=0,
    )


@bot.callback_query_handler(
    func=lambda call: call.data == 'back' and call.from_user.state.startswith(
        'DOCUMENTS:Choice_')
)
@bot.chosen_inline_handler(func=is_state('DOCUMENTS:Select'))
def docs_select(query):
    if type(query) == CallbackQuery:
        storage.update_user_data(query.from_user.id, 'kind', None)
    else:
        storage.update_user_data(query.from_user.id, 'document',
                                 query.result_id)
    Messages.DocumentsKind.send_if_active(query.from_user.id,
                                          set_state='DOCUMENTS:ChoiceKind')


@bot.callback_query_handler(func=is_state('DOCUMENTS:ChoiceKind'))
@bot.message_handler(func=is_state('DOCUMENTS:CertificateSeries'),
                     is_reply_btn_click=Messages.DocumentsCertificateSeries
                     .buttons[0])
@bot.message_handler(
    func=lambda message: message.from_user.state == 'DOCUMENTS:BookSeries',
    is_reply_btn_click=Messages.DocumentsBookSeries.buttons[0]
)
@bot.message_handler(
    func=lambda message: message.from_user.state == 'DOCUMENTS:IdNumber',
    is_reply_btn_click=Messages.DocumentsIdNumber.buttons[0]
)
@bot.message_handler(
    func=lambda message: message.from_user.state == 'DOCUMENTS:Choice_Old',
    is_reply_btn_click=Messages.DocumentsOld.buttons[0]
)
def docs_kind_select(call: Union[CallbackQuery, Message]):
    if type(call) == CallbackQuery:
        storage.update_user_data(call.message.chat.id, 'kind', call.data)
        data = storage.get_user_data(call.message.chat.id)
    else:
        data = storage.get_user_data(call.chat.id)
    if data.get('document') == 'id':
        Messages.DocumentsId.send_if_active(call.from_user.id,
                                            set_state='DOCUMENTS:Choice_ID')
    elif data.get('document') == 'zp':
        Messages.DocumentsZp.send_if_active(call.from_user.id,
                                            set_state='DOCUMENTS:Choice_ZP')
    else:
        Messages.DocumentsOld.send_if_active(
            call.from_user.id,
            set_state=f'DOCUMENTS:Choice_Old'
        )


@bot.callback_query_handler(func=is_state('DOCUMENTS:Choice_ID'))
@bot.message_handler(func=is_state('DOCUMENTS:CertificateNumber'),
                     is_reply_btn_click=Messages.DocumentsCertificateNumber
                     .buttons[0])
@bot.message_handler(
    func=lambda message: storage.get_user_data(
        message.chat.id
    ).get('document') == 'id' and message.from_user.state ==
                         'DOCUMENTS:BookNumber',
    is_reply_btn_click=Messages.DocumentsBookNumber.buttons[0]
)
def docs_id_select_from(call: Union[CallbackQuery, Message]):
    logger.debug('ID PASPORT')
    if type(call) == CallbackQuery:
        data = call.data
        storage.update_user_data(call.from_user.id, 'from_document', data)
    else:
        data = storage.get_user_data(call.from_user.id).get('from_document')
    if data == 'book':
        Messages.DocumentsBookSeries.send_if_active(
            call.from_user.id, set_state='DOCUMENTS:BookSeries'
        )
    elif data == 'id':
        Messages.DocumentsIdNumber.send_if_active(
            call.from_user.id, set_state='DOCUMENTS:IdNumber'
        )
    else:
        Messages.DocumentsCertificateSeries.send_if_active(
            call.from_user.id, set_state='DOCUMENTS:CertificateSeries'
        )


@bot.callback_query_handler(func=is_state('DOCUMENTS:Choice_ZP'))
@bot.message_handler(
    func=lambda message: storage.get_user_data(
        message.chat.id
    ).get('document') == 'zp' and message.from_user.state ==
                         'DOCUMENTS:BookNumber',
    is_reply_btn_click=Messages.DocumentsBookNumber.buttons[0]
)
def docs_zp_select_from(call: Union[CallbackQuery, Message]):
    logger.debug('ZAGRAN')
    if type(call) == CallbackQuery:
        data = call.data
        storage.update_user_data(call.message.chat.id, 'from_document', data)
    else:
        data = storage.get_user_data(call.chat.id).get('from_document')
    if data == 'book':
        Messages.DocumentsBookSeries.send_if_active(
            call.from_user.id, set_state='DOCUMENTS:BookSeries'
        )
    else:
        Messages.DocumentsIdNumber.send_if_active(
            call.from_user.id, set_state='DOCUMENTS:IdNumber'
        )


@bot.message_handler(func=is_state('DOCUMENTS:BookSeries'))
@bot.message_handler(func=is_state('DOCUMENTS:CertificateSeries'))
def docs_number_doc(message: Message):
    storage.update_user_data(message.chat.id, 'series', message.text)
    if message.from_user.state == 'DOCUMENTS:BookSeries':
        Messages.DocumentsBookNumber.send_if_active(
            message.chat.id, set_state='DOCUMENTS:BookNumber'
        )
    else:
        Messages.DocumentsCertificateNumber.send_if_active(
            message.chat.id, set_state='DOCUMENTS:CertificateNumber'
        )


@bot.message_handler(func=is_state('DOCUMENTS:Choice_Old'))
@bot.message_handler(func=is_state('DOCUMENTS:IdNumber'))
@bot.message_handler(func=is_state('DOCUMENTS:BookNumber'))
@bot.message_handler(func=is_state('DOCUMENTS:CertificateNumber'))
def docs_number_doc(message: Message):
    data = storage.get_user_data(message.chat.id)
    logger.debug(data)

    user, _ = User.objects.get_or_create(chat_id=message.chat.id)

    doc, _ = DocState.objects.get_or_create(
        user=user, type_doc=data.get('document'),
        for_doc=data.get('kind'), register_doc=data.get('from_document'),
        series=data.get('series', None), number=message.text
    )
    mes = Messages.DocumentStart.send_if_active(message.chat.id)

    doc_state.apply_async(args=[doc.id, mes.message_id, True])


@bot.callback_query_handler(
    func=lambda call:
    call.data.startswith('doc_') and not call.data.startswith('doc_u#')
)
def docs_subscribe(call: CallbackQuery):
    try:
        markup = call.message.reply_markup
        del markup.keyboard[0]
        bot.edit_message_reply_markup(call.message.chat.id,
                                      call.message.message_id,
                                      reply_markup=markup)
    except Exception as e:
        pass

    try:
        DocState.objects.update_or_create(id=call.data.split('_')[-1],
                                          defaults={'subscribe': True}
                                          )
        Messages.DocumentsSubscribe.send_if_active(
            call.message.chat.id, reply_to_message_id=call.message.message_id
        )
    except Exception as e:
        logger.debug(f'ERROR DocumentsSubs: {e}')


@bot.callback_query_handler(func=is_data('monitoring#inactive'))
@bot.message_handler(
    func=lambda message: message.from_user.state == 'INACTIVE:Number' and
                         storage.get_user_data(message.chat.id).get(
                             'series') is None,
    is_reply_btn_click=Messages.InactiveNumber.buttons[0])
@bot.message_handler(
    func=lambda message: message.from_user.state == 'INACTIVE:Series',
    is_reply_btn_click=Messages.InactiveNumber.buttons[0])
def inactive_docs(msg: Union[CallbackQuery, Message]):
    if type(msg) == CallbackQuery:
        msg = msg.message
        storage.update_user_data(msg.chat.id, 'document', None)
    Messages.Documents_verification.send_if_active(msg.chat.id,
                                                   set_state='INACTIVE:Select')


@bot.inline_handler(func=is_state('INACTIVE:Select'))
def docs_list(query):
    docs = Messages.InactiveTypes.buttons
    locale = query.from_user.lang

    if query.query:
        if locale:
            docs = docs.annotate(
                search=SearchVector('text', f'text_{locale}'),
            ).filter(search__icontains=query.query)
        else:
            docs = docs.filter(text__icontains=query.query)

    inlines = generate_inline_result_from_queryset(
        query_set=docs,
        offset=int(query.offset) if query.offset else 0,
        title=f'text_{locale}' if locale else 'text',
        title_attr=True,
        description=None,
        id_attr='callback_data',
        text=f'text_{locale}' if locale else 'text',
        text_attr=True
    )

    bot.answer_inline_query(
        inline_query_id=query.id,
        results=inlines,
        cache_time=0,
    )


@bot.chosen_inline_handler(func=is_state('INACTIVE:Select'))
@bot.message_handler(
    func=lambda message: message.from_user.state == 'INACTIVE:Number' and
                         storage.get_user_data(message.chat.id).get('series'),
    is_reply_btn_click=Messages.InactiveNumber.buttons[0])
def docs_select(query):
    if type(query) == Message:
        storage.update_user_data(query.from_user.id, 'series', None)
        document = storage.get_user_data(query.from_user.id).get('document')
    else:
        storage.update_user_data(query.from_user.id, 'document',
                                 query.result_id)
        document = query.result_id
    if document == '2' or document == '15' or document == '16':
        Messages.InactiveNumber.send_if_active(query.from_user.id,
                                               set_state='INACTIVE:Number')
    else:
        Messages.InactiveSeries.send_if_active(query.from_user.id,
                                               set_state='INACTIVE:Series')


@bot.message_handler(func=is_state('INACTIVE:Series'))
def inactive_series(message: Message):
    storage.update_user_data(message.chat.id, 'series', message.text)
    Messages.InactiveNumber.send_if_active(message.chat.id,
                                           set_state='INACTIVE:Number')


@bot.message_handler(func=is_state('INACTIVE:Number'))
def inactive_number(message: Message):
    data = storage.get_user_data(message.chat.id)
    logger.debug(data)

    user, _ = User.objects.get_or_create(chat_id=message.chat.id)
    doc, _ = InactiveDocument.objects.get_or_create(
        user=user, type_doc=data.get('document'), series=data.get('series'),
        number=message.text
    )

    mes = Messages.InactiveStart.send_if_active(message.chat.id)
    inactive_doc.apply_async(args=[doc.id, mes.message_id, True])


@bot.callback_query_handler(
    func=lambda call: call.data.startswith('inactive_'))
def inactive_subscribe(call: CallbackQuery):
    try:
        markup = call.message.reply_markup
        del markup.keyboard[0]
        bot.edit_message_reply_markup(call.message.chat.id,
                                      call.message.message_id,
                                      reply_markup=markup)
    except Exception as e:
        pass

    try:
        InactiveDocument.objects.update_or_create(id=call.data.split('_')[-1],
                                                  defaults={'subscribe': True}
                                                  )
        Messages.InactiveSubscribe.send_if_active(
            call.message.chat.id, reply_to_message_id=call.message.message_id
        )
    except Exception as e:
        logger.debug(f'ERROR DocumentsSubs: {e}')
