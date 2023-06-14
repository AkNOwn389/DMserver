from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from.models import OnlineUser
from django.core.cache import cache
from django.contrib.auth.models import AbstractBaseUser, User
from .dbManager import getOnlineUser, ImOnline, ImOffline
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
        try:
            self.user:AbstractBaseUser = self.scope['user']
            if self.user.is_authenticated:
                await database_sync_to_async(self.addOnlineUser)(self.user)
                await self.accept()
                await self.send(text_data=json.dumps({"message": "connection created"}))
                await ImOnline(self.user)
                print(f"\033[1;92m{self.user} \033[1;95mis connected login status is active\033[1;97m")
        except:
            self.disconnect()
            
    async def disconnect(self, close_code):
            await database_sync_to_async(self.deleteOnlineUser)(self.user)
            await ImOffline(self.user)
            print(f"\033[1;91mLog out\033[1;93m: \033[1;92m{self.user}\033[1;97m", close_code)

    async def receive(self, text_data):
            await self.send(text_data=json.dumps({"message": str(text_data)}))
            
            
            
class OnlineUserCosummer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.user:AbstractBaseUser = self.scope['user']
            if self.user.is_authenticated:
                await self.accept()
                data = await getOnlineUser(user = self.user)
                text = {
                    "data": data,
                    "message": "connection created",
                    "type": "connectionCreated",
                    }
                await self.send(text_data=json.dumps(text))
                self.room = str(f"room_{self.user.username}")
                await self.channel_layer.group_add(self.room, self.channel_name)
        except:
            self.disconnect(5001)
    
    async def receive(self, text_data=None, bytes_data=None):
          return await super().receive(text_data, bytes_data)
      
    async def disconnect(self, code):
        self.channel_layer.group_discard(self.room, self.channel_name)
        return await super().disconnect(code)
      
    async def new_online_user(self, event:dict):
        await self.send(text_data=json.dumps(event))
    
    async def new_offline_user(self, event:dict):
        await self.send(text_data=json.dumps(event))               