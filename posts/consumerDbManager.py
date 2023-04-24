from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from typing import Set, Awaitable, Optional, Tuple
from django.contrib.auth.models import AbstractBaseUser
from chats.models import UploadedFile
from .models import Comment
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from django.db.models.fields.files import ImageFieldFile
from .serializers import PostCommentSerializer
from .models import Comment

@database_sync_to_async
def get_user_by_pk(pk: str) -> Awaitable[Optional[AbstractBaseUser]]:
    return User.objects.filter(pk=pk).first()


@database_sync_to_async
def get_file_by_id(file_id: str) -> Awaitable[Optional[UploadedFile]]:
    try:
        f = UploadedFile.objects.filter(id=file_id).first()
    except ValidationError:
        f = None
    return f

@database_sync_to_async
def commentToJson(comment:Comment) -> Awaitable[Optional[dict]]:
    data = PostCommentSerializer(comment).data


@database_sync_to_async
def get_serialize_profile(user:str) -> Awaitable[Optional[dict]]:
    return ProfileSerializer(Profile.objects.get(user=User.objects.get(pk = user))).data

@database_sync_to_async
def save_comment(post_id:str, text: str, user: AbstractBaseUser, type:int, avatar:ImageFieldFile) -> Awaitable[Optional[Comment]]:
    return Comment.objects.create(post_id = post_id, comments=text, user=user, type=type, avatar = avatar)