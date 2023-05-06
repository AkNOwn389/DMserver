from django.shortcuts import render
from posts.models import Post
from profiles.models import Profile
from rest_framework.views import APIView
from posts.serializers import PostSerializer
from django.contrib.auth.models import User
from posts.models import Post, LikePost
from profiles.models import  Profile
from users.models import FollowerCount
from profiles.views import getAvatarByUsername
from time_.get_time import getStringTime
from users.views import isFollowed, isFollower
from profiles.serializers import ProfileSerializer
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from notifications.models import MyNotification
from posts.serializers import ImagesSerializer, PostUploader, PostCommentSerializer
from notifications.views import LikeNotificationView, CommentNotificationView
from posts.models import Comment as CommentTable, LikeComment as Like_Comment , Image as PostImage, Videos as PostVideos
from django.db.models import Q, F
from .comment_types import CommentTypes, CommentStrType
from news.models import News
from django.db import transaction
from django.core.files.base import ContentFile
from io import BytesIO
import cloudinary
from .commentManager import save_comment
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import enum, json




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






class SendComment(APIView):
    def getRoom(self, postId):
        if Post.objects.filter(id = postId).exists():
            return True
        elif News.objects.filter(id = postId).exists():
            return True
        else:
            return False
    def CreateComment(self, postId:str, comment:str, user:AbstractBaseUser, commentType:int) -> CommentTable:
        profile = Profile.objects.get(user = user)
        return save_comment(post_id=postId, text=comment, user=user, type=commentType, avatar=profile.profileimg)
    
    def commentSender(self, room:str, serializeComment:dict, comment_type:str) -> None:
        channel_layer = get_channel_layer()
        group_name = room
        serializeComment['type'] = comment_type
        print(serializeComment)
        async_to_sync(channel_layer.group_send)(group_name, serializeComment)
        return

    def commentWithImage(self, request, file) -> Response:
        comment = request.data['comment']
        post_id = request.data['postId']
        cmt:CommentTable = self.CreateComment(
            postId=post_id,
            comment=comment,
            user = request.user,
            commentType=2)
        cmt.image.create(image = file)
        cmt.save()
        serializeComment:PostCommentSerializer = PostCommentSerializer(cmt)
        self.commentSender(room=post_id,
                           serializeComment=serializeComment.data,
                           comment_type="new_image_comment")
        serializeComment.data['user_full_name'] = Profile.objects.get(user = User.objects.get(username = serializeComment.data['user'])).name
        serializeComment.data['Followed'] = isFollowed(request.user, serializeComment.data['user'])
        serializeComment.data['Follower'] = isFollower(request.user, serializeComment.data['user'])
        serializeComment.data['created'] = getStringTime(serializeComment.data['created'])
        serializeComment.data['me'] = True
        return Response({
            "status": True,
            "status_code": 200,
            "message": "comment_Created",
            "data": serializeComment.data
        })
    def commentWithVideo(self, request, file) -> Response:
        comment = request.data['comment']
        post_id = request.data['postId']
        cmt:CommentTable = self.CreateComment(
            postId=post_id,
            comment=comment,
            user = request.user,
            commentType=3)
        cmt.video.create(videos = file)
        cmt.save()
        serializeComment:PostCommentSerializer = PostCommentSerializer(cmt)
        self.commentSender(room=post_id,
                           serializeComment=serializeComment.data,
                           comment_type="new_video_comment")
        serializeComment.data['user_full_name'] = Profile.objects.get(user = User.objects.get(username = serializeComment.data['user'])).name
        serializeComment.data['Followed'] = isFollowed(request.user, serializeComment.data['user'])
        serializeComment.data['Follower'] = isFollower(request.user, serializeComment.data['user'])
        serializeComment.data['created'] = getStringTime(serializeComment.data['created'])
        serializeComment.data['me'] = True
        return Response({
            "status": True,
            "status_code": 200,
            "message": "comment_Created",
            "data": serializeComment.data
        })
    def commentNaNatural(self, request) -> Response:
        comment = request.data['comment']
        post_id = request.data['postId']
        cmt:CommentTable = self.CreateComment(
            postId=post_id,
            comment=comment,
            user = request.user,
            commentType=1)
        serializeComment:PostCommentSerializer = PostCommentSerializer(cmt)
        self.commentSender(room=post_id,
                           serializeComment=serializeComment.data,
                           comment_type="new_comment_message")
        serializeComment.data['user_full_name'] = Profile.objects.get(user = User.objects.get(username = serializeComment.data['user'])).name
        serializeComment.data['Followed'] = isFollowed(request.user, serializeComment.data['user'])
        serializeComment.data['Follower'] = isFollower(request.user, serializeComment.data['user'])
        serializeComment.data['created'] = getStringTime(serializeComment.data['created'])
        serializeComment.data['me'] = True
        return Response({
            "status": True,
            "status_code": 200,
            "message": "comment_Created",
            "data": serializeComment.data
        })

    def put(self, request, commentType):
        user:AbstractBaseUser = request.user
        if user.is_authenticated:
            if self.getRoom(postId=request.data['postId']):
                if commentType == CommentStrType.FileComment:
                    file = request.FILES.get("video")
                    print("uploading comment video")
                    return self.commentWithVideo(request=request, file=file)
                elif commentType == CommentStrType.ImageComment:
                    print("uploading image in comment")
                    file = request.FILES.get("image")
                    return self.commentWithImage(request=request, file=file)
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
        user:AbstractBaseUser = request.user
        if user.is_authenticated:
            if self.getRoom(postId=request.data['postId']):
                if commentType == CommentStrType.TEXT:
                    return self.commentNaNatural(request=request)
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
    success = {'status': True,'status_code': 200, 'message': 'success'}
    def getPostData(self, post_id):
        try:
            post = Post.objects.get(id=post_id)
            return post
        except:
            pass
        try:
            post = Post.objects.get(images_url__id=str(post_id))
            return post.images_url.get(id = post_id)
        except:
            pass

        return None
    def post(self, request):
        if request.user.is_authenticated:
            user:AbstractBaseUser = request.user
            user_profile = Profile.objects.get(user = user)
            comment = request.data['comment']
            post_id = request.data['post_id']
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync

            channel_layer = get_channel_layer()
            group_name = 'my_group'

            # Send a message to the group
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'my.message',
                    'text': 'Hello, group!'
                }
            )
            try:
                post = self.getPostData(post_id=post_id)
                if post == None:
                    err_404['message'] = "post doest not exists"
                    return JsonResponse(err_404)
            except Post.DoesNotExist:
                err_404['message'] = "post doest not exists"
                return JsonResponse(err_404)
            try:
                a = CommentTable.objects.create(post_id = post_id, avatar = user_profile.profileimg, comments = comment, user = user, type = 1)
                a.save()
                post.NoOfcomment = post.NoOfcomment+1
                post.save()
                CommentNotificationView.Notify(post_id=post_id, request=request)
                serializer = PostCommentSerializer(a)
                self.success['message'] = 'success'
                self.success['data'] = serializer.data
                self.success['data']['user_full_name'] = Profile.objects.get(user = User.objects.get(username = serializer.data['user'])).name
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
            page = page*16
            comment = CommentTable.objects.filter(post_id = id).order_by("-created")
            if len(comment) == 0:
                success['message'] = 'success'
                success['data'] = []
                return Response({
                    'status': True,
                    'status_code':200,
                    'message': 'success',
                    'data': []
                })
            serialiser = PostCommentSerializer(comment[int(page)-16:int(page)], many = True)
            for i in serialiser.data:
                i['user_full_name'] = Profile.objects.get(user = User.objects.get(username = i['user'])).name
                i['Followed'] = isFollowed(request.user, i['user'])
                i['Follower'] = isFollower(request.user, i['user'])
                i['created'] = getStringTime(i['created'])
                i['isLike'] = True if Like_Comment.objects.filter(user = request.user, commentId = i['id']).first() else False
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
