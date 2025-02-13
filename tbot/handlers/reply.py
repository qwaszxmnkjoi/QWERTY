from django.contrib.postgres.search import SearchVector
from loguru import logger
from telebot.types import Message

from customer.models import News, User
from tbot.messages import Messages
from tbot.storage import storage
from tbot_messages.bot import bot
from tbot_messages.utils import generate_inline_result_from_queryset, is_state


@bot.message_handler(is_reply_btn_click=Messages.Menu.buttons[3])
def migration(message: Message):
    Messages.Migration.send_if_active(message.chat.id, set_state='migration')


@bot.inline_handler(func=is_state('migration'))
def citizenship(query):
    locale = query.from_user.lang

    btns = Messages.Citizenship.buttons
    if query.query:
        btns = btns.annotate(
            search=SearchVector('text', f'text_{locale}'),
        ).filter(search__icontains=query.query)

    inlines = generate_inline_result_from_queryset(
        query_set=btns,
        offset=int(query.offset) if query.offset else 0,
        title=f'text_{locale}' if locale else 'text',
        title_attr=True,
        description=None,
        text=[f'text_{locale}' if locale else 'text',
              f'url_{locale}' if locale else 'url'],
        text_attr=True
    )
    bot.answer_inline_query(
        inline_query_id=query.id,
        results=inlines,
        cache_time=0,
    )


@bot.message_handler(is_reply_btn_click=Messages.Menu.buttons[6])
def cross_the_bord(message: Message):
    Messages.CrossingTheBorder.send_if_active(message.chat.id)
