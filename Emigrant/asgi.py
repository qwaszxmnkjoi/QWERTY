import os


from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Emigrant.settings')

http_app = get_asgi_application()

from customer.consumers import chat_consumer


application = ProtocolTypeRouter({
    'http': http_app,
    'websocket': AllowedHostsOriginValidator(
        URLRouter([
            # URLRouter just takes standard Django path() or url() entries.
            path('chat/stream/', chat_consumer),
        ])
    )

})
