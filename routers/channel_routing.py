from django.urls import re_path, path, include

from users import consumer
from chats import consumers
from notifications.notification_consumer import NotificationBadgeSocket

websocket_urlpatterns = [
    re_path(r'^chat_ws$', consumers.ChatConsumer.as_asgi()),
    path('user/connect', consumer.LoginSocket.as_asgi()),
    path('notificationBadge', NotificationBadgeSocket.as_asgi())
]