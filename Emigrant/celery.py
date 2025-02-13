import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Emigrant.settings')

celery_app = Celery('Emigrant')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.conf.beat_schedule = {
    'check_user_subs': {
        'task': 'check_user_subs',
        'schedule': crontab(minute='0', hour='*/1'),
    },
    'subs': {
        'task': 'scrap_subs',
        'schedule': crontab(minute='0', hour='9')
    }
}

celery_app.autodiscover_tasks()
