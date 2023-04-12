from channels.db import database_sync_to_async
from typing import Set, Awaitable, Optional, Tuple
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import message as UserMessage


@database_sync_to_async
def get_user_by_username(username: str) -> Awaitable[Optional[AbstractBaseUser]]:
    return User.objects.filter(username=username).first()

@database_sync_to_async
def get_user_by_id(id: str) -> Awaitable[Optional[AbstractBaseUser]]:
    return User.objects.filter(id = id).first()

@database_sync_to_async
def mark_message_as_read(mid: int) -> Awaitable[None]:
    return UserMessage.objects.filter(id=mid).update(read=True)
