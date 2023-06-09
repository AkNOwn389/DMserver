from django.urls import re_path, path, include

from users import consumer as user_consumer
from chats import consumers as chat_consumer
from notifications.notification_consumer import NotificationBadgeSocket
from comments.consumer import CommentConsumer

websocket_urlpatterns = [
    path('ws/chat/socketTo=<str:user>', chat_consumer.ChatConsumer.as_asgi()),
    path('ws/commentRoom/<str:postId>', CommentConsumer.as_asgi()),
    path('user/connect', user_consumer.LoginSocket.as_asgi()),
    path('user/online-users', user_consumer.OnlineUserCosummer.as_asgi()),
    path('notificationBadge', NotificationBadgeSocket.as_asgi()),
    path('ws/chatPage', chat_consumer.MessagePageView.as_asgi()),
]
