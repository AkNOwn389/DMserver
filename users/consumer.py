from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from.models import OnlineUser
import json

class LoginSocket(AsyncWebsocketConsumer):
    def deleteOnlineUser(self, user):
            try:
                OnlineUser.objects.get(user=user).delete()
            except:
                pass
    def addOnlineUser(self, user):
            try:
                OnlineUser.objects.create(user=user)
            except:
                pass
    async def connect(self):
            self.user = self.scope['user']
            if self.user.is_authenticated:
                await database_sync_to_async(self.addOnlineUser)(self.user)
                await self.accept()
                await self.send(text_data=json.dumps({"message": "connection created"}))

    async def disconnect(self, close_code):
            await database_sync_to_async(self.deleteOnlineUser)(self.user)
            print("socket close: ", close_code)

    async def receive(self, text_data):
            await self.send(text_data=json.dumps({"message": str(text_data)}))
                        