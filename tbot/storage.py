from django.conf import settings

from tbot_messages.storage import RedisStorage

if settings.DEV_MODE:
    storage = RedisStorage('localhost', 6379, 1)
else:
    storage = RedisStorage('redis', 6379, 1)

