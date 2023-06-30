import json
from typing import Optional, Dict, Tuple
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, JsonWebsocketConsumer
from django.contrib.auth.models import User, AbstractBaseUser
from users.models import OnlineUser
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from .serializers import MessagesSerialiser
from .models import PrivateRoom, RoomManager
from .managers import get_chat_page_channel_name, get_chat_user_room_name
from asgiref.sync import sync_to_async
from django.db.models import Q
from .db_operations import get_unread_count, get_file_by_id, save_text_message, mark_message_as_read, \
    get_serialize_profile, get_user_profile, get_user_by_pk, serializeMessage, getMessageData, getMainPageView
from .errors import ErrorTypes
from .models import PrivateMessage as UserMessage
from .message_types import MessageTypeFileMessage, MessageTypeMessageRead, MessageTypes, MessageTypeTextMessage, \
    Optional, OutgoingEventIsTyping, OutgoingEventMessageRead, OutgoingEventStoppedTyping, ChatPageTypes, ChatPageViewTypes
from chats.models import RoomManager
from time_.get_time import getStringTime
from .errors import ErrorTypes, ErrorDescription
from django.conf import settings
import logging



logger = logging.getLogger('chats.consumers')
TEXT_MAX_LENGTH = getattr(settings, 'TEXT_MAX_LENGTH', 65535)
UNAUTH_REJECT_CODE: int = 4001
ERROR_404 = 404


class UserChattingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        return await super().connect()
    async def receive(self, text_data=None, bytes_data=None):
        return await super().receive(text_data, bytes_data)
    async def disconnect(self, code):
        return await super().disconnect(code)
    #handle user request
    async def handle_request(self, json_data: dict, data_type: str):
        pass
    #functions
    async def new_message(self, event: dict):
        pass
    async def isTyping(self, event: dict):
        pass
    async def stopTyping(self, event: dict):
        pass
    async def new_user_online(self, event: dict):
        pass
    async def new_user_offline(self, event:dict):
        pass
    async def new_reactions(self, event: dict):
        pass
    async def new_image_message(self, event: dict):
        pass
    async def new_video_message(self, event: dict):
        pass



class MessagePageViewV2(AsyncWebsocketConsumer):
    async def handle_receive__data(self, text_data_json: dict, message_type: str):
        if message_type == ChatPageViewTypes.refresh:
            msg_lists = await getMainPageView(user=self.user)
            c = await sync_to_async(self.serialize)(msg_lists, 1)
            for i in c:
                data = await getMessageData(self.user, i)
                i.update(data)
                
            text: dict = {
                'status': True,
                'status_code': 200,
                'data': c,
                'hasMorePage': True if len(c) >= 16 else False,
                'message': 'success'
            }
            await self.send(json.dumps(text))
            return None
        elif message_type == ChatPageViewTypes.nextPage:
            page:int = text_data_json['page']
            msg_lists = await getMainPageView(user=self.user)
            c = await sync_to_async(self.serialize)(msg_lists, page)
            for i in c:
                data = await getMessageData(self.user, i)
                i.update(data)
            text: dict = {
                'status': True,
                'status_code': 200,
                'data': c,
                'hasMorePage': True if len(c) >= 16 else False,
                'message': 'success'
            }
            await self.send(json.dumps(text))
            return None
            
    async def connect(self):
        self.user: AbstractBaseUser = self.scope['user']
        if self.user.is_authenticated:
            await self.accept()
            self.room = get_chat_page_channel_name(self.user.username)
            self.channel_layer.group_add(self.room, self.channel_name)
            msg_lists = await getMainPageView(user=self.user)
            c = await sync_to_async(self.serialize)(msg_lists, 1)
            for i in c:
                data = await getMessageData(self.user, i)
                i.update(data)
                
            text: dict = {
                'status': True,
                'status_code': 200,
                'data': c,
                'hasMorePage': True if len(c) >= 16 else False,
                'message': 'connected'
            }
            await self.send(json.dumps(text))
            
            
        else:
            print(f"Rejecting unauthenticated user with code {UNAUTH_REJECT_CODE}")
            await self.close(code=UNAUTH_REJECT_CODE)
            
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        if not "type" in text_data_json:
            self.send(json.dumps({"status": False,
                                  "status_code": 403,
                                "message": "invalid data type"}))
        message_type = text_data_json['type']
        
        if not isinstance(message_type, str):
            self.send(json.dumps({"status": False,
                                  "status_code": 403,
                                "message": "invalid data type"}))
        error = await self.handle_receive__data(text_data_json=text_data_json, message_type=message_type)
        if error is not None:
            text = {
                "status": False,
                "status_code": 403,
                "message": str(error)
            }
            self.send(json.dumps(text))
    async def disconnect(self, code):
        try:
            print(f"{self.user} is disconnected with close code of {code}")
            await self.channel_layer.group_discard(self.room, self.channel_name)
        except Exception as e:
            print(f"Exception call in disconnect: {e}")
        return await super().disconnect(code)

    async def new_message(self, event: dict):
        await self.send(json.dumps(event))

    def serialize(self, msgList: list[UserMessage], page: int):
        limit: int = settings.PAGE_LIMIT
        return MessagesSerialiser(msgList[int(page) - int(limit):int(page)], many=True).data