from channels.db import database_sync_to_async
from .models import PrivateMessage as message, UploadedFile
from typing import Set, Awaitable, Optional, Tuple
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import PrivateMessage as MessageModel
from .serializers import MessagesSerialiser
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from .models import RoomManager

@database_sync_to_async
def get_user_by_pk(pk: str) -> Awaitable[Optional[AbstractBaseUser]]:
    return User.objects.filter(username=pk).first()

@database_sync_to_async
def get_user_profile(user:AbstractBaseUser) -> Awaitable[Optional[Profile]]:
    return Profile.objects.filter(user=user).first()

@database_sync_to_async
def get_serialize_profile(user:AbstractBaseUser) -> Awaitable[Optional[dict]]:
    return ProfileSerializer(Profile.objects.get(user = user)).data

@database_sync_to_async
def get_file_by_id(file_id: str) -> Awaitable[Optional[UploadedFile]]:
    try:
        f = UploadedFile.objects.filter(id=file_id).first()
    except ValidationError:
        f = None
    return f

# @database_sync_to_async
# def mark_message_as_read(mid: int, sender_pk: str, recipient_pk: str):
#     return MessageModel.objects.filter(id__lte=mid,sender_id=sender_pk, recipient_id=recipient_pk).update(read=True)

@database_sync_to_async
def mark_message_as_read(mid: str, sender:AbstractBaseUser, receiver:AbstractBaseUser) -> Awaitable[bool]:
    message:MessageModel = MessageModel.objects.filter(id=mid, sender = sender, receiver = receiver).first()
    if message is None:
        return False
    message.update(seen = True)
    return True


@database_sync_to_async
def get_unread_count(sender:AbstractBaseUser, receiver:AbstractBaseUser) -> Awaitable[int]:
    return int(RoomManager.get_unread_count_for_dialog_with_user(sender = sender, recipient = receiver))

@database_sync_to_async
def serializeMessage(message:MessageModel) -> Awaitable[dict]:
    return MessagesSerialiser(message).data


@database_sync_to_async
def save_text_message(message: str, from_: AbstractBaseUser, to: AbstractBaseUser) -> Awaitable[MessageModel]:
    return MessageModel.objects.create(message_body=message, sender=from_, receiver=to)