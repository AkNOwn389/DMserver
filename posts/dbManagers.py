from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from comments.models import LikeComment as Like_Comment
from news.models import News
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .types import PostType
from .models import Post

def getUser(user):
    try:
        a = User.objects.get(id=user)
        return a
    except:
        pass
    try:
        a = User.objects.get(username=user)
        return a
    except:
        pass
    try:
        a = User.objects.get(email=user)
        return a
    except:
        pass

    return None


def sendGroup(user: AbstractBaseUser, postId: str, id: str):
    channel_layer = get_channel_layer()
    group_name = postId
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "user": user.username,
            "data_type": 7,
            "commentId": str(id),
            "type": "new_comment_deleted"
        })
    return


def getPostData(post_id):
    try:
        post = Post.objects.get(id=post_id)
        return post
    except:
        pass
    try:
        post = Post.objects.get(images_url__id=str(post_id))
        return post.images_url.get(id=post_id)
    except:
        pass
    try:
        post = News.objects.get(id=str(post_id))
        return post
    except:
        pass
    return None


def GetPostData(post_id, post_type):
    if post_type == PostType.POST:
        try:
            # print("Post method call")
            post = Post.objects.get(id=post_id)
            return post
        except Post.DoesNotExist:
            return None

    elif post_type == PostType.NEWSPOST:
        try:
            # print("news post method call")
            post = News.objects.get(id=post_id)
            return post
        except News.DoesNotExist:
            return None

    elif post_type == PostType.POSTIMAGE:
        try:
            # print("post image method call")
            post = Post.objects.get(images_url__id=str(post_id))
            return post.images_url.get(id=post_id)
        except Post.DoesNotExist:
            return None

    elif post_type == PostType.VIDEO:
        try:
            # print("video  method call")
            post = Post.objects.get(id=post_id)
            return post
        except Post.DoesNotExist:
            return None

    else:
        return None

def getCommentReactions(Id):
    return {"Like": len(Like_Comment.objects.filter(commentId=Id, reactionType="T")),
            "Love": len(Like_Comment.objects.filter(commentId=Id, reactionType="L")),
            "Happy": len(Like_Comment.objects.filter(commentId=Id, reactionType="H")),
            "Sad": len(Like_Comment.objects.filter(commentId=Id, reactionType="S")),
            "Wow": len(Like_Comment.objects.filter(commentId=Id, reactionType="W")),
            "Angry": len(Like_Comment.objects.filter(commentId=Id, reactionType="A"))}
