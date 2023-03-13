from django.urls import re_path, path, include

from users import consumer
from chats import consumers

websocket_urlpatterns = [
    path('chats/', consumers.ChatConsumer.as_asgi()),
    path('user/connect', consumer.LoginSocket.as_asgi()),
]
