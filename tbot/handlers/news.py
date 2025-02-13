from typing import Union

from loguru import logger
from telebot.types import CallbackQuery, Message

from customer.models import News, NewsContent, User
from tbot.messages import Messages
from tbot.storage import storage
from tbot_messages.bot import bot


@bot.callback_query_handler(func=lambda call: call.data.startswith('news'))
@bot.message_handler(is_reply_btn_click=Messages.Menu.buttons[1])
@bot.message_handler(is_reply_btn_click=Messages.DetailNews.buttons[0])
@bot.message_handler(is_reply_btn_click=Messages.NewsSendTitle.buttons[2])
def news_message(message: Union[Message, CallbackQuery], page: int = 0):
    if type(message) == CallbackQuery:
        logger.debug(message.data)
        page = int(message.data.split('#')[-1])
        message = message.message
        bot.delete_message(message.chat.id, message.message_id)

    if storage.get_user_data(message.chat.id).get('get_news'):
        page = storage.get_user_data(message.chat.id).get('news_page', 0)

    storage.update_user_data(message.chat.id, 'news_page', page)
    storage.update_user_data(message.chat.id, 'get_news', False)

    user, _ = User.objects.update_or_create(
        chat_id=message.chat.id,
        defaults={
            'username': message.from_user.username,
        }
    )
    news = News.objects.filter(
        status='publish', language__contains=user.language
    )
    if news:
        cur_count = page * 5
        next_count = cur_count + 5 if cur_count + 5 <= len(news) \
            else len(news)

        for obj in news[cur_count:next_count]:
            if user.unsubscribe_news:
                Messages.NewsTitleUnsub.send_if_active(
                    message.chat.id,
                    format_map={'title': obj.title}
                )
            else:
                Messages.NewsTitle.send_if_active(
                    message.chat.id,
                    format_map={'title': obj.title}
                )
            Messages.News.send_if_active(
                message.chat.id,
                photo=obj.image.read()
                if obj.image and '.mp4' not in obj.image.path else None,
                video=obj.image.read()
                if obj.image and '.mp4' in obj.image.path else None,
                format_keyboard_map={'news_id': obj.id},
                custom_markup=False if obj.content.all() else None,
                format_map={'description': obj.text}
            )

        Messages.NewsShowMore.send_if_active(
            message.chat.id,
            format_map={'current': next_count, 'total': len(news)},
            format_keyboard_map={'next_count': len(news)-next_count,
                                 'page': page + 1},
            custom_markup=False if len(news) > next_count else None

        )
    else:
        if user.unsubscribe_news:
            Messages.NotFoundNewsUnsubscribe.send_if_active(message.chat.id)
        else:
            Messages.NotFoundNews.send_if_active(message.chat.id)


@bot.callback_query_handler(
    func=lambda call: call.data.startswith('get_news')
)
def get_news(call: CallbackQuery):
    news_contents = NewsContent.objects.filter(
        news_id=call.data.split('#')[-1]
    )
    send = True
    if storage.get_user_data(call.message.chat.id).get('news_page') is not \
            None:
        storage.update_user_data(call.message.chat.id, 'get_news', True)
        send = False

    for content in news_contents:
        if send:
            Messages.NewsSendDetail.send_if_active(
                call.message.chat.id,
                photo=content.image.read()
                if content.image and '.mp4' not in content.image.path else None,
                video=content.image.read()
                if content.image and '.mp4' in content.image.path else None,
                format_map={'description': content.text}
            )
        else:
            Messages.DetailNews.send_if_active(
                call.message.chat.id,
                photo=content.image.read()
                if content.image and '.mp4' not in content.image.path else None,
                video=content.image.read()
                if content.image and '.mp4' in content.image.path else None,
                format_map={'description': content.text}
            )


@bot.message_handler(
    is_reply_btn_click=Messages.NotFoundNews.buttons[0]
)
@bot.message_handler(is_reply_btn_click=Messages.Subscribe.buttons[0])
@bot.message_handler(is_reply_btn_click=Messages.NewsTitle.buttons[0])
@bot.message_handler(is_reply_btn_click=Messages.NewsSendTitle.buttons[0])
def unsub_news(message: Message):
    user, _ = User.objects.update_or_create(
        chat_id=message.chat.id,
        defaults={
            'username': message.from_user.username,
            'unsubscribe_news': True
        }
    )
    Messages.Unsubscribe.send_if_active(message.chat.id)


@bot.message_handler(
    is_reply_btn_click=Messages.NotFoundNewsUnsubscribe.buttons[0]
)
@bot.message_handler(is_reply_btn_click=Messages.Unsubscribe.buttons[0])
@bot.message_handler(is_reply_btn_click=Messages.NewsTitleUnsub.buttons[0])
def sub_news(message: Message):
    user, _ = User.objects.update_or_create(
        chat_id=message.chat.id,
        defaults={
            'username': message.from_user.username,
            'unsubscribe_news': False
        }
    )
    Messages.Subscribe.send_if_active(message.chat.id)
