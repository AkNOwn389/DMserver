
from django.contrib.auth.models import User
from posts.models import Post
from profiles.models import Profile
from time_.get_time import getStringTime
from users.views import isFollowed, isFollower
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Comment as CommentTable, Comment
from .serializers import PostCommentSerializer, LikesCommentSerializer
from notifications.views import CommentNotificationView
from comments.models import LikeComment as Like_Comment
from django.db.models import Q, F
from .comment_types import CommentStrType
from news.models import News
from .commentManager import save_comment
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from typing import Union, Optional
success = {"status": True, "status_code": 200}
err_401 = {"status": False, "status_code": 401}
err_402 = {"status": False, "status_code": 402}
err_403 = {"status": False, "status_code": 403}
err_404 = {"status": False, "status_code": 404}
err_405 = {"status": False, "status_code": 405}
err_406 = {"status": False, "status_code": 406}
err_407 = {"status": False, "status_code": 407}
err_408 = {"status": False, "status_code": 408}
err_409 = {"status": False, "status_code": 409}
err_410 = {"status": False, "status_code": 410}
err_411 = {"status": False, "status_code": 411}
err_412 = {"status": False, "status_code": 412}
err_413 = {"status": False, "status_code": 413}
err_414 = {"status": False, "status_code": 414}
err_415 = {"status": False, "status_code": 415}
err_416 = {"status": False, "status_code": 416}


def commentSender(room: str, serializeComment: dict, comment_type: str) -> None:
    channel_layer = get_channel_layer()
    group_name = str(room)
    serializeComment['type'] = comment_type
    async_to_sync(channel_layer.group_send)(group_name, serializeComment)
    return


def CreateComment(postId: str, comment: str, user: AbstractBaseUser, commentType: int) -> Comment:
    profile = Profile.objects.get(user=user)
    return save_comment(post_id=postId, text=comment, user=user, Type=commentType, avatar=profile.profileimg)


def getRoom(postId):
    if Post.objects.filter(id=postId).exists():
        return True
    elif News.objects.filter(id=postId).exists():
        return True
    elif Post.objects.filter(images_url__id=postId).exists():
        return True
    else:
        return False


def commentWithImage(request, file) -> Response:
    comment = request.data['comment']
    post_id = request.data['postId']
    cmt: CommentTable = CreateComment(
        postId=post_id,
        comment=comment,
        user=request.user,
        commentType=2)
    cmt.image.create(image=file)
    cmt.save()
    serializeComment:dict = PostCommentSerializer(cmt).data
    commentSender(room=post_id,
                  serializeComment=serializeComment,
                  comment_type="new_image_comment")
    serializeComment['user_full_name'] = Profile.objects.get(
        user=User.objects.get(username=serializeComment['user'])).name
    serializeComment['Followed'] = isFollowed(request.user, serializeComment['user'])
    serializeComment['Follower'] = isFollower(request.user, serializeComment['user'])
    serializeComment['created'] = getStringTime(serializeComment['created'])
    serializeComment['is_like'] = False
    serializeComment['me'] = True
    return Response({
        "status": True,
        "status_code": 200,
        "message": "comment_Created",
        "data": serializeComment
    })


def commentWithVideo(request, file) -> Response:
    comment = request.data['comment']
    post_id = request.data['postId']
    cmt: CommentTable = CreateComment(
        postId=post_id,
        comment=comment,
        user=request.user,
        commentType=3)
    cmt.video.create(videos=file)
    cmt.save()
    serializeComment:dict = PostCommentSerializer(cmt).data
    commentSender(room=post_id,
                  serializeComment=serializeComment,
                  comment_type="new_video_comment")
    serializeComment['user_full_name'] = Profile.objects.get(
        user=User.objects.get(username=serializeComment['user'])).name
    serializeComment['Followed'] = isFollowed(request.user, serializeComment['user'])
    serializeComment['Follower'] = isFollower(request.user, serializeComment['user'])
    serializeComment['created'] = getStringTime(serializeComment.data['created'])
    serializeComment['is_like'] = False
    serializeComment['me'] = True
    return Response({
        "status": True,
        "status_code": 200,
        "message": "comment_Created",
        "data": serializeComment
    })


def commentNaNatural(request) -> Response:
    comment = request.data['comment']
    post_id = request.data['postId']
    cmt: CommentTable = CreateComment(
        postId=post_id,
        comment=comment,
        user=request.user,
        commentType=1)
    serializeComment: dict = PostCommentSerializer(cmt).data
    commentSender(room=post_id,
                  serializeComment=serializeComment,
                  comment_type="new_comment_message")
    serializeComment['user_full_name'] = Profile.objects.get(
        user=User.objects.get(username=serializeComment['user'])).name
    serializeComment['Followed'] = isFollowed(request.user, serializeComment['user'])
    serializeComment['Follower'] = isFollower(request.user, serializeComment['user'])
    serializeComment['created'] = getStringTime(serializeComment['created'])
    serializeComment['is_like'] = False
    serializeComment['me'] = True
    print(serializeComment)
    return Response({
        "status": True,
        "status_code": 200,
        "message": "comment_Created",
        "data": serializeComment
    })


class SendComment(APIView):
    def put(self, request, commentType):
        user: AbstractBaseUser = request.user
        if user.is_authenticated:
            if getRoom(postId=request.data['postId']):
                if commentType == CommentStrType.FileComment:
                    file = request.FILES.get("video")
                    print("uploading comment video")
                    return commentWithVideo(request=request, file=file)
                elif commentType == CommentStrType.ImageComment:
                    print("uploading image in comment")
                    file = request.FILES.get("image")
                    return commentWithImage(request=request, file=file)
                else:
                    return Response({
                        "status": False,
                        "status_code": 403,
                        "message": "file not supported"
                    })

            else:
                return Response({
                    "status": False,
                    "status_code": 404,
                    "message": "post is not valid"
                })

    def post(self, request, commentType):
        user: AbstractBaseUser = request.user
        if user.is_authenticated:
            if getRoom(postId=request.data['postId']):
                if commentType == CommentStrType.TEXT:
                    print(request.data)
                    return commentNaNatural(request=request)
                else:
                    return Response({
                        "status": False,
                        "status_code": 403,
                        "message": "file not supported"
                    })

            else:
                return Response({
                    "status": False,
                    "status_code": 404,
                    "message": "post is not valid"
                })


class CommentView(APIView):
    success = {'status': True, 'status_code': 200, 'message': 'success'}

    def getPostData(self, post_id:str):
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

        return None

    def post(self, request):
        if request.user.is_authenticated:
            user: AbstractBaseUser = request.user
            user_profile = Profile.objects.get(user=user)
            comment = request.data['comment']
            post_id = request.data['post_id']
            try:
                post = self.getPostData(post_id=post_id)
                if post == None:
                    err_404['message'] = "post doest not exists"
                    return JsonResponse(err_404)
            except Post.DoesNotExist:
                err_404['message'] = "post doest not exists"
                return JsonResponse(err_404)
            try:
                a = CommentTable.objects.create(post_id=post_id, avatar=user_profile.profileimg, comments=comment,
                                                user=user, type=1)
                a.save()
                post.NoOfcomment = post.NoOfcomment + 1
                post.save()
                CommentNotificationView.Notify(post_id=post_id, request=request)
                serializer = PostCommentSerializer(a)
                self.success['message'] = 'success'
                self.success['data'] = serializer.data
                self.success['data']['user_full_name'] = Profile.objects.get(
                    user=User.objects.get(username=serializer.data['user'])).name
                self.success['data']['Followed'] = isFollowed(request.user, serializer.data['user'])
                self.success['data']['Follower'] = isFollower(request.user, serializer.data['user'])
                self.success['data']['created'] = getStringTime(serializer.data['created'])
                self.success['data']['me'] = True
                return Response(self.success)
            except:
                err_403['message'] = 'system failure'
                return Response(err_403)

        err_401['message'] = 'invalid user'
        return JsonResponse(err_401)

    def get(self, request, id, page):
        if request.user.is_authenticated:
            page = page * 16
            comment = CommentTable.objects.filter(post_id=id).order_by("-created")
            if len(comment) == 0:
                success['message'] = 'success'
                success['data'] = []
                return Response({
                    'status': True,
                    'status_code': 200,
                    'message': 'success',
                    'data': []
                })
            serialiser = PostCommentSerializer(comment[int(page) - 16:int(page)], many=True)
            for i in serialiser.data:
                i['user_full_name'] = Profile.objects.get(user=User.objects.get(username=i['user'])).name
                i['Followed'] = isFollowed(request.user, i['user'])
                i['Follower'] = isFollower(request.user, i['user'])
                i['created'] = getStringTime(i['created'])
                if Like_Comment.objects.filter(user=request.user,commentId=i['id']).exists():
                    i['is_like'] = True
                    i['reactionType'] = LikesCommentSerializer(Like_Comment.objects.filter(commentId=i['id'], user=request.user).first()).data['reactionType']
                else:
                    i['is_like'] = False
                i['me'] = True if i['user'] == request.user.username else False

            return Response({
                'status': True,
                'status_code': 200,
                'message': 'success',
                'hasMorePage': True if len(serialiser.data) == 16 else False,
                'data': serialiser.data
            })

        err_401['message'] = 'invalid user'
        return Response(err_401)
