from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from typing import Set, Awaitable, Optional, Tuple
from django.contrib.auth.models import AbstractBaseUser
from chats.models import UploadedFile
from posts.models import Comment
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from django.db.models.fields.files import ImageFieldFile
from posts.serializers import PostCommentSerializer
from posts.models import Comment
from posts.models import Post
from news.models import News

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