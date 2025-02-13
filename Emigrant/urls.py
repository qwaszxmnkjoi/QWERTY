from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from payment.views import get_payment
from tbot_messages.views import webhook
from tbot.views import chat_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/<str:country>/<str:category>/<str:chat_id>', chat_view, name='chat_by_category'),
    path('paym', get_payment),
    path('paym/<str:backend>', get_payment),
    path('', webhook),
]
if settings.DEV_MODE:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
