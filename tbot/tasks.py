from customer.models import News, User
from Emigrant.celery import celery_app as app
from tbot.messages import Messages
from tbot.storage import storage
from tbot_messages.bot import bot


@app.task(name='send_news')
def send_news_as_notification(news_id):
    try:
        news = News.objects.get(id=news_id)
        users = User.objects.filter(
            unsubscribe_news=False,
            language__in=eval(news.language)
        ).exclude(chat_id='').exclude(chat_id=None).exclude(blocked=True)
        photo = news.image.read(

        ) if news.image and '.mp4' not in news.image.path else None
        video = news.image.read(

        ) if news.image and '.mp4' in news.image.path else None
        for user in users:
            Messages.NewsSendTitle.send_if_active(
                user.chat_id, format_map={'title': news.title}
            )
            Messages.News.send_if_active(
                user.chat_id,
                photo=photo,
                video=video,
                format_keyboard_map={'news_id': news.id},
                custom_markup=False if news.content.all() else None,
                format_map={'description': news.text}
            )
        news.status = 'publish'
        news.save()
        return f'News With id {news_id} Send Successful'
    except News.DoesNotExist:
        return f'News with id {news_id} DoesNotExist'
