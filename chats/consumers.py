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
from .managers import MessageManager
from asgiref.sync import sync_to_async
from django.db.models import Q
from .db_operations import get_unread_count, get_file_by_id, save_text_message, mark_message_as_read, \
    get_serialize_profile, get_user_profile, get_user_by_pk, serializeMessage, getMessageData
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


def getProfile(user):
    return ProfileSerializer(Profile.objects.get(user=user)).data


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.chatMate = None
        self.connected = None
        self.user = None

    def SocksUser(self, user: AbstractBaseUser, chatMate: str):
        self.connected = False
        try:
            user2 = User.objects.get(username=chatMate)
        except User.DoesNotExist:
            return None
        if user.username == chatMate:
            return None
        self.connected = True
        self.chatMate = user2
        return RoomManager().getOrCreateOneToOneRoom(user1=user, user2=user2).encode('utf-8').decode()

    def getMessagePagination(self, page: int, user1: AbstractBaseUser, user2: AbstractBaseUser):
        messages = RoomManager().getMessagePagination(page=page, user1=user1, user2=user2)
        serializeMessage = MessagesSerialiser(messages, many=True)
        return serializeMessage.data

    def createTextMessage(self, creator: AbstractBaseUser, receiver: AbstractBaseUser, message: str) -> dict:
        msg = UserMessage.objects.create(sender=creator, receiver=receiver, message_body=message)
        msg.save()
        serializeMessage = MessagesSerialiser(msg)
        return serializeMessage.data

    async def connect(self):
        self.user: AbstractBaseUser = self.scope['user']
        self.user2 = self.scope['url_route']['kwargs']['user']

        if self.user.is_authenticated:
            print("connection from: ", self.user)
            room = await database_sync_to_async(self.SocksUser)(self.user, self.user2)
            if self.connected:
                print(f"{self.user} connected in: {self.chatMate}")
                await self.accept()
                self.room = room
                await self.channel_layer.group_add(self.room, self.channel_name)
                userProfile = await sync_to_async(getProfile)(self.user)
                chatMateProfile = await sync_to_async(getProfile)(self.chatMate)
                text = {
                    'status': True,
                    'status_code': 200,
                    'type': "handshake",
                    'message': f'connected to {self.user2}',
                    'data': {
                        'username': self.user.username,
                        'id': self.user.id
                    },
                    'chatmate': {
                        'id': self.chatMate.id,
                        'username': self.chatMate.username
                    }
                }
                text['chatmate'].update(chatMateProfile)
                text['data'].update(userProfile)
                await self.send(text_data=json.dumps(text))

            else:
                print(f"Rejecting invalid user with code {ERROR_404}")
                logger.info(f"Rejecting invalid user with code {UNAUTH_REJECT_CODE}")
                await self.close(code=ERROR_404)
        else:
            logger.info(f"Rejecting unauthenticated user with code {UNAUTH_REJECT_CODE}")
            await self.close(code=UNAUTH_REJECT_CODE)

    async def disconnect(self, close_code):
        try:
            print(f"{self.user} is disconnected in {self.chatMate} with close code of {close_code}")
            await self.channel_layer.group_discard(self.room, self.channel_name)
        except Exception as e:
            print(f"Exception call in disconnect: {e}")

    async def handle_received_message(self, message_type: MessageTypes, data: Dict[str, str]) -> Optional[
        ErrorDescription]:
        logger.info(f"Received message type {message_type.name} from user {self.user} with data {data}")
        if message_type == MessageTypes.IsTyping:
            print(f"User {self.user.username} is typing, sending 'is_typing' to {self.room}")
            await self.channel_layer.group_send(str(self.room),
                                                OutgoingEventIsTyping(user=str(self.user.username))._asdict())
            return None
        elif message_type == MessageTypes.TypingStopped:
            print(
                f"User {self.user.username} has stopped typing, sending 'stopped_typing' to {self.room}")
            await self.channel_layer.group_send(str(self.room),
                                                OutgoingEventStoppedTyping(user=str(self.user.username))._asdict())
            return None
        elif message_type == MessageTypes.TextMessage:
            data: MessageTypeTextMessage
            if 'message_body' not in data:
                return ErrorTypes.MessageParsingError, "'message_body' not present in data"
            elif data['message_body'] == '':
                return ErrorTypes.TextMessageInvalid, "'message_body' should not be blank"
            elif len(data['message_body']) > TEXT_MAX_LENGTH:
                return ErrorTypes.TextMessageInvalid, "'message_body' is too long"
            elif not isinstance(data['message_body'], str):
                return ErrorTypes.TextMessageInvalid, "'message_body' should be a string"
            else:
                text = data['message_body']
                print(f"Validation passed, sending text message from {self.user} to {self.chatMate}")

            print(f"Will save text message from {self.user} to {self.chatMate}")
            data: UserMessage = await save_text_message(message=text, from_=self.user, to=self.chatMate)
            message = await serializeMessage(data)
            message['date_time'] = getStringTime(message['date_time'])
            message['type'] = "new_message"
            print(f"sending {message} in room:{self.room}")
            await self.channel_layer.group_send(self.room, message)

    # Receive message from WebSocket

    async def receive(self, text_data):
        print(f"Receive fired {text_data}")
        error: Optional[ErrorDescription] = None
        try:
            text_data_json = json.loads(text_data)
            logger.info(f"From {self.user} received '{text_data_json}")
            if not ('message_type' in text_data_json):
                error = (ErrorTypes.MessageParsingError, "message_type not present in json")
            else:
                message_type = text_data_json['message_type']
                if not isinstance(message_type, int):
                    error = (ErrorTypes.MessageParsingError, "message_type is not an int")
                else:
                    try:
                        message_type_case: MessageTypes = MessageTypes(message_type)
                        error = await self.handle_received_message(message_type_case, text_data_json)
                    except ValueError as e:
                        error = (ErrorTypes.MessageParsingError, f"message_type decoding error - {e}")
        except json.JSONDecodeError as e:
            error = (ErrorTypes.MessageParsingError, f"jsonDecodeError - {e}")
        if error is not None:
            error_data = {
                'message_type': MessageTypes.ErrorOccurred,
                'error': error
            }
            logger.info(f"Will send error {error_data} to {self.room}")
            await self.send(text_data=json.dumps(error_data))

    async def new_message(self, event: dict):
        await self.send(text_data=json.dumps(event))

    async def stopped_typing(self, event: dict):
        print(event)
        await self.send(text_data=OutgoingEventStoppedTyping(**event).to_json())

    async def is_typing(self, event: dict):
        print(event)
        await self.send(text_data=OutgoingEventIsTyping(**event).to_json())





    
    
    


class MessagePageView(AsyncWebsocketConsumer):
    async def connect(self):
        self.user: AbstractBaseUser = self.scope['user']
        if self.user.is_authenticated:
            await self.accept()
            data = {
                'status': True,
                'status_code': 200,
                'message': 'connected'
            }
            await self.send(json.dumps(data))
        else:
            print(f"Rejecting unauthenticated user with code {UNAUTH_REJECT_CODE}")
            await self.close(code=UNAUTH_REJECT_CODE)

    async def receive(self, text_data: dict = None, bytes_data=None):
        text_data: dict = json.loads(text_data)
        if "type" in text_data:
            type: int = text_data['type']
            await self.__handle_receive(type, text_data)

    async def __handle_receive(self, type: ChatPageTypes, text_data: dict):
        if type == ChatPageTypes.SyncPage:
            msg_lists = await sync_to_async(MessageManager().getMainPageView)(user=self.user)
            c = await sync_to_async(self.serialize)(msg_lists, 1)
            for i in c:
                data = await sync_to_async(self.getMessageData)(i)
                i.update(data)
            text: dict = {
                'status': True,
                'status_code': 200,
                'type': 1,
                'data': c,
                'hasMorePage': True if len(c) >= 16 else False
            }
            await self.send(json.dumps(text))

    def getMessageData(self, event: dict):
        event['username'] = event['receiver'] if event['sender'] == self.user.username else event['sender']
        event['sender_full_name'] = Profile.objects.get(user=User.objects.get(username=event['sender'])).name
        event['receiver_full_name'] = Profile.objects.get(user=User.objects.get(username=event['receiver'])).name
        event['user_full_name'] = Profile.objects.get(user=User.objects.get(username=event['username'])).name
        event['user_avatar'] = \
        ProfileSerializer(Profile.objects.get(user=User.objects.get(username=event['username']))).data['profileimg']
        event['message_lenght'] = len(
            UserMessage.objects.filter(sender=User.objects.get(username=event['username']), receiver=self.user))
        event['type'] = 1
        if event['sender'] == self.user.username:
            event['message_body'] = f"You: {event['message_body']}"
        return event

    def serialize(self, msgList: list[UserMessage], page: int):
        limit: int = settings.PAGE_LIMIT
        return MessagesSerialiser(msgList[int(page) - int(limit):int(page)], many=True).data

    async def disconnect(self, code):
        print(f"{self.user} is disconnected")
        return await super().disconnect(code)
