import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-oqpx*=g6t-ng!s%ob4*r8pe3am#@@4s6l9_$0@stz391*om)2z'

DEBUG = True
DEV_MODE = False

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://bot.ggs.com.ua']

INSTALLED_APPS = [
    'channels',
    'mptt',
    'versatileimagefield',
    'sass_processor',
    'daphne',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',

    'tbot_messages',
    'customer',
    'tbot',
    'payment',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'Emigrant.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {'customer': 'customer.templatetags'},
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

# WSGI_APPLICATION = 'Emigrant.wsgi.application'
ASGI_APPLICATION = 'Emigrant.asgi.application'

if DEV_MODE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'Emigrant',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '8238',
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('POSTGRES_DB'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': os.getenv('POSTGRES_HOST'),
            'PORT': '5432',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'
LANGUAGES = (
    ('uk', 'Ukrainian'),
    ('ru', 'Russian'),
    ('en', 'English'),
)
TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
SASS_PROCESSOR_ROOT = STATIC_ROOT
# if DEV_MODE:
#     STATICFILES_DIRS = [BASE_DIR / 'static']
#     SASS_PROCESSOR_ROOT = STATICFILES_DIRS[0]
# else:
#     STATIC_ROOT = BASE_DIR / 'static'
#     STATICFILES_DIRS = STATIC_ROOT
#     SASS_PROCESSOR_ROOT = STATICFILES_DIRS[0]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

CELERY_BROKER_URL = f'redis://{os.getenv("REDIS_HOST", "localhost")}:{os.getenv("REDIS_PORT", 6379)}/0'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

CELERY_TIMEZONE = 'Europe/Kiev'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

from tbot.storage import storage
from tbot.translations import translate

BOT_STORAGE = storage
BOT_HANDLERS = [
    'tbot.handlers'
]
BOT_MESSAGES = translate

RECAPTCHA_TOKEN = '40633031f634b5876d50943f960cf061'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.getenv("REDIS_HOST", "localhost"), os.getenv("REDIS_PORT", 6379))],
        },
    },
}
