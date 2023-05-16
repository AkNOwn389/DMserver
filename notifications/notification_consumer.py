from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import MyNotification
from django.contrib.auth.models import AbstractBaseUser
from chats.models import PrivateMessage, RoomManager
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .dbManager import getOrCreateNotificationChannel, chatBadge, notifBadge
import json





class NotificationBadgeSocket(AsyncWebsocketConsumer):

    # Default method
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room = None
        self.user = None

    async def connect(self):
        self.user:AbstractBaseUser = self.scope['user']
        if self.user.is_authenticated:
            await self.accept()
            self.room = await database_sync_to_async(getOrCreateNotificationChannel)(user=self.user)
            await self.channel_layer.group_add(self.room, self.channel_name)
            await self.send(text_data=json.dumps({"message": "connection created"}))
            chat = await database_sync_to_async(chatBadge)(self.user)
            notif = await database_sync_to_async(notifBadge)(self.user)
            await self.send(text_data=json.dumps({
                'status': True,
                'status_code': 200,
                'type': 'new_notification_badge',
                'notification': notif,
                'chat': chat}))

    async def disconnect(self, close_code):
        print(f"socket close: {self.user}", close_code)
        await self.channel_layer.group_discard(self.room, self.channel_name)

    async def receive(self, text_data):
        res = json.loads(text_data)
        if res['message'] == "notificationBadgeNumber":
            chat = await database_sync_to_async(chatBadge)(self.user)
            notif = await database_sync_to_async(notifBadge)(self.user)
            await self.send(text_data=json.dumps({
                'status': True,
                'status_code': 200,
                'notification': notif,
                'chat': chat}))

    async def new_notification(self, event: dict):
        await self.send(text_data=json.dumps(event))

    async def new_chat(self, event: dict):
        await self.send(text_data=json.dumps(event))
        
    async def new_notification_badge(self, event:dict):
        await self.send(text_data=json.dumps(event))
