from django.urls import re_path, path, include
from chats import routing
from users import websocket
websocket_urlpatterns = [
    path('', routing.websocket_urlpatterns),
    path('user/', websocket.websocket_urlpatterns),
]
