from django.urls import reverse
from loguru import logger
from telebot.types import Message, InlineKeyboardButton, WebAppInfo

from customer.models import Category, Country
from tbot.messages import Messages
from tbot_messages.bot import bot
from tbot_messages.utils import generate_inline_result_from_queryset, is_state

name_map = {
    'ua': 'name_uk',
    'en': 'name_en',
    'ru': 'name'
}


@bot.message_handler(is_reply_btn_click=Messages.Menu.buttons[2])
def chat_message(message: Message):
    Messages.Chat.send_if_active(message.chat.id, set_state='chat')


@bot.inline_handler(func=is_state('chat'))
def select_chat(query):
    countries = Country.objects.filter(name__icontains=query.query)
    lang = query.from_user.lang or 'ru'
    name_attr = name_map[lang]

    inlines = generate_inline_result_from_queryset(
        query_set=countries,
        offset=int(query.offset) if query.offset else 0,
        title=name_attr,
        title_attr=True,
        description=None,
        text=name_attr,
        text_attr=True
    )
    bot.answer_inline_query(
        inline_query_id=query.id,
        results=inlines,
        cache_time=0,
    )


def build_cat_buttons(country_slug, categories, chat_id, name_attr: str = 'name'):
    buttons = []
    for cat in categories:
        if cat.is_leaf_node():
            chat_url = reverse('chat_by_category', args=(country_slug, cat.slug, chat_id))
            web_app = WebAppInfo(url=f'https://{bot.config.webhook_url}{chat_url}')
            callback_data = None
        else:
            callback_data = f'category#{cat.id}'
            web_app = None
        buttons.append([
            InlineKeyboardButton(
                text=getattr(cat, name_attr, 'name'),
                callback_data=callback_data,
                web_app=web_app
            )
        ])

    return buttons


def get_country_text(country_id, chat_id, message_id: int = None, lang: str = 'en'):
    try:
        country = Country.objects.get(id=country_id)
        categories = Category.objects.filter(country=country, parent__isnull=True)
        name_attr = name_map[lang]

        Messages.GetCountry.send_if_active(
            user_id=chat_id,
            format_map={'country': getattr(country, name_attr, 'name')},
            add_markup_buttons=build_cat_buttons(country.slug, categories, chat_id, name_attr)
        )
        try:
            bot.delete_message(chat_id, message_id)
        except Exception:
            pass
    except Exception as e:
        logger.debug(e)


@bot.chosen_inline_handler(func=is_state('chat'))
def user_select_chat(query):
    return get_country_text(query.result_id, query.from_user.id, lang=query.from_user.lang or 'ru')


@bot.callback_query_handler(func=lambda call: call.data.startswith('country#'))
def get_country(call):
    return get_country_text(call.data.split('#')[-1], call.from_user.id, call.message.message_id, call.from_user.lang or 'ru')


@bot.callback_query_handler(func=lambda call: call.data.startswith('category#'))
def category_ancestors(call):
    split_data = call.data.split('#')
    obj_id = split_data[-1]
    lang = call.from_user.lang or 'ru'
    chat_id = call.from_user.id
    if len(split_data) == 3:
        return get_country_text(obj_id, chat_id, call.message.message_id, lang)
    else:
        try:
            parent_cat = Category.objects.get(id=obj_id)
            categories = Category.objects.filter(parent=parent_cat).select_related('country')
            country = categories[0].country
            name_attr = name_map[lang]
            category_text = ' >'.join(getattr(cat, name_attr, 'name') for cat in parent_cat.ancestors)

            Messages.GetCategory.send_if_active(
                user_id=chat_id,
                format_map={'country': getattr(country, name_attr, 'name'), 'category': category_text},
                format_keyboard_map={'cat_id': f'country#{country.id}' if not parent_cat.is_leaf_node() else parent_cat.id},
                add_markup_buttons=build_cat_buttons(country.slug, categories, chat_id, name_attr)
            )
            try:
                bot.delete_message(chat_id, call.message.id)
            except Exception:
                pass
        except Exception as e:
            logger.debug(e)
