from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from typing import Set, Awaitable, Optional, Tuple, Any
from django.contrib.auth.models import AbstractBaseUser
from chats.models import UploadedFile
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from django.db.models.fields.files import ImageFieldFile
from comments.serializers import PostCommentSerializer
from comments.models import Comment
from posts.models import Post, Image
from news.models import News


def save_comment(post_id: str, text: str, user: AbstractBaseUser, Type: int, avatar: ImageFieldFile) -> Any | None:
    if Post.objects.filter(id=post_id).exists():
        post: Post = Post.objects.get(id=post_id)
        post.NoOfComment = post.NoOfComment + 1
        post.save()
    elif News.objects.filter(id=post_id).exists():
        news: News = News.objects.get(id=post_id)
        news.NoOfComment = news.NoOfComment + 1
        news.save()
    elif Post.objects.filter(images_url__id=post_id).exists():
        post = Post.objects.get(images_url__id=post_id)
        post_image:Image = post.images_url.get(id=post_id)
        post_image.NoOfcomment = post_image.NoOfcomment + 1
        post_image.update()
    else:
        return None
    return Comment.objects.create(post_id=post_id, comments=text, user=user, comment_type=Type, avatar=avatar)
