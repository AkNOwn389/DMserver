from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import MyNotification
from chats.models import message
import json

class NotificationBadgeSocket(AsyncWebsocketConsumer):
    def notifBadge(self, user):
        notif = MyNotification.objects.filter(user = user, seen = False)
        return len(notif) if len(notif) < 100 else 99

    def chatBadge(self, user):
        notif = message.objects.filter(receiver = user, seen = False)
        return len(notif) if len(notif) < 100 else 99
    

    #Default method
    async def connect(self):
            self.user = self.scope['user']
            if self.user.is_authenticated:
                await self.accept()
                await self.send(text_data=json.dumps({"message": "connection created"}))

    async def disconnect(self, close_code):
            print(f"socket close: {self.user}", close_code)

    async def receive(self, text_data):
            res = json.loads(text_data)
            print(res)
            if res['message'] == "notificationBadgeNumber":
                chat = await database_sync_to_async(self.chatBadge)(self.user)
                notif = await database_sync_to_async(self.notifBadge)(self.user)
                await self.send(text_data=json.dumps({
                        'status': True,
                        'status_code': 200,
                        'notification': notif,
                        'chat': chat}))