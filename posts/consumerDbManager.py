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
from posts.models import Post
from news.models import News

@database_sync_to_async
def get_user_by_pk(pk: str) -> Awaitable[Optional[AbstractBaseUser]]:
    return User.objects.filter(username=pk).first()


@database_sync_to_async
def get_file_by_id(file_id: str) -> Awaitable[Optional[UploadedFile]]:
    try:
        f = UploadedFile.objects.filter(id=file_id).first()
    except ValidationError:
        f = None
    return f

@database_sync_to_async
def commentToJson(comment:Comment) -> Awaitable[Optional[dict]]:
    return PostCommentSerializer(comment).data


@database_sync_to_async
def get_serialize_profile(user:str) -> Awaitable[Optional[dict]]:
    return ProfileSerializer(Profile.objects.get(user=User.objects.get(username = user))).data

@database_sync_to_async
def get_user_profile(user:AbstractBaseUser) -> Awaitable[Optional[Profile]]:
    return Profile.objects.get(user = user)

@database_sync_to_async
def save_comment(post_id:str, text: str, user: AbstractBaseUser, type:int, avatar:ImageFieldFile) -> Awaitable[Optional[Comment]]:
    if Post.objects.filter(id = post_id).exists():
        post:Post = Post.objects.get(id = post_id)
        post.NoOfcomment = post.NoOfcomment + 1
        post.save()
    elif News.objects.filter(id = post_id).exists():
        news:News = News.objects.get(id = post_id)
        news.noOfComment = news.noOfComment + 1
        news.save()
    else:
        return None
    return Comment.objects.create(post_id = post_id, comments=text, user=user, comment_type=type, avatar = avatar)