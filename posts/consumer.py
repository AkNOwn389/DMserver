import json
from typing import Optional, Dict, Tuple
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, JsonWebsocketConsumer
from django.contrib.auth.models import AbstractBaseUser
from .consumerErrorTypes import ErrorDescription, ErrorTypes
from .models import Post, Comment
from users.views import isFollowed, isFollower
from asgiref.sync import sync_to_async
from time_.get_time import getStringTime

from .serializers import PostCommentSerializer

#----------
from .comment_types import CommentTypes, CommentTypesCommentMessage, OutgoingEventIsTyping,  Optional, OutgoingEventStoppedTyping

from .consumerDbManager import get_file_by_id, get_user_by_pk, save_comment, get_serialize_profile, commentToJson

TEXT_MAX_LENGTH = 10000



class CommentConsumer(AsyncWebsocketConsumer):
    def getRoom(self, postId):
        return Post.objects.filter(id = postId).exists()
    
    async def connect(self):
        self.user:AbstractBaseUser = self.scope['user']
        room = self.scope['url_route']['kwargs']['postId']
        if self.user.is_authenticated:
            if await database_sync_to_async(self.getRoom)(room):
                self.room = room
                await self.channel_layer.group_add(self.room, self.channel_name)
                await self.accept()
                await self.send(json.dumps({
                    'status':True,
                    'status_code':200,
                    'message':'connected',
                }))
            self.disconnect(404)
        self.disconnect(401)

    async def _handle_received(self, dataType:int, data:dict):
        if dataType == CommentTypes.CommentMessage:
            data: CommentTypesCommentMessage
            if 'comment' not in data:
                return ErrorTypes.MessageParsingError, "'text' not present in data"
            elif data['comment'] == '':
                return ErrorTypes.TextMessageInvalid, "'text' should not be blank"
            elif len(data['comment']) > TEXT_MAX_LENGTH:
                return ErrorTypes.TextMessageInvalid, "'text' is too long"
            elif not isinstance(data['comment'], str):
                return ErrorTypes.TextMessageInvalid, "'text' should be a string"
            else:
                text = data['comment']
                comment_data:Comment = await save_comment(text, from_=self.user, to=self.user, type = 1)
                serializeComment:dict = await commentToJson(comment_data)
                await self.channel_layer.group_send(
                    self.room,
                    serializeComment
                    )

        elif dataType == CommentTypes.CommentCreated:
            pass
        elif dataType == CommentTypes.FileComment:
            pass
        elif dataType == CommentTypes.IsTyping:
            pass
        elif dataType == CommentTypes.StopTyping:
            pass
        else:
            pass

    async def receive(self, text_data=None, bytes_data=None):
        print(f"Receive fired")
        error: Optional[ErrorDescription] = None
        try:
            text_data_json = json.loads(text_data)
            print(f"From {self.room} received '{text_data_json}")
            if not ('msg_type' in text_data_json):
                error = (ErrorTypes.MessageParsingError, "msg_type not present in json")
            else:
                msg_type = text_data_json['msg_type']
                if not isinstance(msg_type, int):
                    error = (ErrorTypes.MessageParsingError, "msg_type is not an int")
                else:
                    try:
                        msg_type_case: CommentTypes = CommentTypes(msg_type)
                        error = await self._handle_received(msg_type_case, text_data_json)
                    except ValueError as e:
                        error = (ErrorTypes.MessageParsingError, f"msg_type decoding error - {e}")
                        
        except json.JSONDecodeError as e:
            error = (ErrorTypes.MessageParsingError, f"jsonDecodeError - {e}")
        if error is not None:
            error_data = {
                'data_type': CommentTypes.ErrorOccurred,
                'error': error
            }
            print(f"Will send error {error_data} to {self.room}")
            await self.send(text_data=json.dumps(error_data))

    async def disconnect(self, code):
        return await super().disconnect(code)
    
    #EVENT
    async def new_comment_message(self, event:dict):
        user:str = event['user']
        serializeProfile = await get_serialize_profile(user)
        event['user_full_name'] = serializeProfile['name']
        event['Followed'] = await database_sync_to_async(isFollowed)(self.user, event['user'])
        event['Follower'] = await database_sync_to_async(isFollower)(self.user, event['user'])
        event['created'] = await getStringTime(event['created'])
        event['me'] = True if event['user'] == self.user.username else False
        await self.send(text_data=json.dumps(event))
    