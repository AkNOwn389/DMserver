
from .serializers import PostSerializer
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
from .serializers import ImagesSerializer, PostUploader, LikesPostSerializer
from notifications.views import LikeNotificationView, CommentNotificationView
from .models import  Image as PostImage, Videos as PostVideos
from comments.models import LikeComment as Like_Comment, Comment
from comments.comment_types import CommentTypes, CommentStrType
from comments.serializers import PostCommentSerializer
from django.db.models import Q, F
from news.models import News
from PIL import Image as ImagePIL, ImageFile
from django.db import transaction
from io import BytesIO, StringIO
from django.core.files import File
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
import cloudinary
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import enum

# Create your views here.
#class response
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

class PostType(enum.StrEnum):
        POST = "posts"
        NEWSPOST = "news"
        POSTIMAGE = "postImage"
        VIDEO = "videos"
class PostReactionType(enum.StrEnum):
    LIKE = "Like"
    LOVE = "Love"
    HAPPY = "Happy"
    WOW = "Wow"
    ANGRY = "Angry"
    SAD = "Sad"
class ReactOrUnReact(enum.StrEnum):
    REACT = "react"
    UNREACT = "unReact"

class ChangePrivacy(APIView):
    def get(self, request, id, privacy):
        if request.user.is_authenticated:
            try:
                posts = Post.objects.get(id = id, creator = request.user)
            except:
                return Response({
                    'status': False,
                    'status_code': 404,
                    'message': 'posts not exists'
                })
            if privacy == "Public":
                posts.privacy = "P"
            elif privacy == "Friends":
                posts.privacy = "F"
            elif privacy == "Only-Me":
                posts.privacy = "O"
            else:
                pass
            posts.save()
            return Response({
                'status':True,
                'status_code': 200,
                'message': 'success'
            })
        return Response({'status': False,
                         'status_code': 401,
                         'message': 'invalid user'
                         })

class DeletePost(APIView):
    def get(self, request, postId):
        if request.user.is_authenticated:
            try:
                posts = Post.objects.get(id = postId, creator = request.user)
            except Post.DoesNotExist:
                return Response({
                    'status': False,
                    'status_code': 404,
                    'message': 'posts not exists'
                })
            try:
                for i in posts.images_url.all():
                    img = PostImage.objects.get(id = str(i))
                    try:
                        cloudinary.uploader.destroy(img.public_id)
                    except:
                        pass
                    img.delete()
                for i in posts.videos_url.all():
                    img = PostVideos.objects.get(id = str(i))
                    try:
                        cloudinary.uploader.destroy(img.public_id)
                    except:
                        pass
                    img.delete()
            except:
                pass
            posts.delete()
            return Response({
                'status': True,
                'status_code': 200,
                'message': 'posts deleted.'
            })
        
        return Response({'status': False,
                         'status_code': 401,
                         'message': 'invalid user'
                         })


class GetPostDataById(APIView):
    success = {"status": True, "status_code": 200}
    def get(self, request, postId):
        if request.user.is_authenticated:
            post = Post.objects.filter(Q(id = postId) | Q(images_url__id = postId) | Q(videos_url__id = postId)).first()
            if post is None:
                self.success['status'] = False
                self.success['message'] = 'Not found'
                self.success['status_code'] = 404
                return Response(data=self.success)
            serialiser = PostSerializer(post)
            success['message'] = "success"
            success['data'] = serialiser.data
            success['data']['creator_avatar'] = ProfileSerializer(Profile.objects.get(user = User.objects.get(username = serialiser.data['creator']))).data['profileimg']
            success['data']['your_avatar'] = ProfileSerializer(Profile.objects.get(user = User.objects.get(username = request.user.username))).data['profileimg']
            success['data']['created_at'] = getStringTime(serialiser.data['created_at'])
            success['data']['is_like'] = True if LikePost.objects.filter(post_id=serialiser.data['id'], username=request.user).first() else False
            success['data']['reactionType'] = LikesPostSerializer(LikePost.objects.filter(post_id=serialiser.data['id'], username=request.user).first()).data['reactionType']
            for i in success['data']['image_url']:
                if LikePost.objects.filter(post_id=i['id'], username=request.user).exists():
                    i['is_like'] = True
                    i['reactionType'] = LikesPostSerializer(LikePost.objects.get(post_id=i['id'], username=request.user)).data['reactionType']
                else:
                    i['is_like'] = False
            for i in success['data']['videos_url']:
                if LikePost.objects.filter(post_id=i['id'], username=request.user).exists():
                    i['is_like'] = True
                    i['reactionType'] = LikesPostSerializer(LikePost.objects.get(post_id=i['id'], username=request.user)).data['reactionType']
                else:
                    i['is_like'] = False
            return Response(success)

#@transaction.atomic
class upload(APIView):
    def getType(self, request):
        images= request.FILES.getlist('image',)
        videos = request.FILES.getlist('video',)
        if images == [] and videos == []:
            return None, None, 0
        if images == [] and videos != []:
            return None, videos, 5
        if images != [] and videos == []:
            return images, None, 2
        
        return images, videos, 5
    def put(self, request):
        if request.user.is_authenticated:
            isError = False
            images, videos, TYPE = self.getType(request=request)
            if images == None and videos == None and TYPE == 0:
                return Response({
                        'status': False,
                        'status_code': 403,
                        'message': 'media type not supported'
                    })
            user = request.user
            data = request.data
            user_profile = Profile.objects.get(user = user)
            """
            if images != None:
                for i in images:
                    y = {"image": i}
                    x = ImagesSerializer(data = y)
                    if x.is_valid(raise_exception=True):
                        pass
                    else:
                        isError = True
                        """
                    
            if not isError:
                try:
                    postToUpload = Post.objects.create(creator = user,
                                            creator_full_name=user_profile.name,
                                            description = data['caption'],
                                            media_type=TYPE,
                                            privacy=data['privacy'])
                except KeyError:
                    return Response({
                        'status': False,
                        'status_code': 403,
                        'message': 'invalid cridentials'
                    })
                try:
                    if TYPE == 2 or TYPE == 5:
                        if images != None:
                            for i in images:
                                postToUpload.images_url.create(image = i)
                    if TYPE == 5:
                        for i in videos:
                            postToUpload.videos_url.create(videos = i)
                    postToUpload.save()
                except Exception as e:
                    print(e)
                    try:
                        Post.objects.get(id = postToUpload.id).delete()
                    except:
                        pass
                    return Response({
                        'status': False,
                        'status_code': 403,
                        'message': str(e)
                    })
                return JsonResponse({'status': True,'status_code': 200, 'message': 'upload data success'})
            else:
                return JsonResponse({'status': False,'status_code': 200, 'message': 'invalid data'})
            
        return JsonResponse({'status': False, 'status_code': 401, 'message': 'invalid user'})
    

class uploadTextPost(APIView):
    def post(self, request):
        me = request.user
        if me.is_authenticated:
            try:
                user = Profile.objects.get(user=request.user)
                data = {"creator": request.user.id, 'creator_full_name': user.name, "description": request.data['caption'], 'media_type': 1, 'privacy': request.data['privacy']}
                serializer = PostUploader(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return JsonResponse({'status': True,'status_code': 200, 'message': 'upload success'})
                
            except KeyError:
                return JsonResponse({'status': False,'status_code': 200, 'message': 'key Error'})
            
        return JsonResponse({'status': False, 'status_code': 401, 'message': 'invalid user'})



class is_like(APIView):
    def post(self, request):
        post_id = request.data['post_id']
        user = request.user
        like_filter = LikePost.objects.filter(post_id=post_id, username=user).first()
        if like_filter is None:
            return JsonResponse({'status': True, 'message': False})
        else:
            return JsonResponse({'status': True, 'message': True})



class Like_Post(APIView):
    def GetPostData(self, post_id, post_type):
        if post_type == PostType.POST:
            try:
                #print("Post method call")
                post = Post.objects.get(id=post_id)
                return post
            except Post.DoesNotExist:
                return None
            
        elif post_type == PostType.NEWSPOST:
            try:
                #print("news post method call")
                post =  News.objects.get(id = post_id)
                return post
            except News.DoesNotExist:
                return None
            
        elif post_type == PostType.POSTIMAGE:
            try:
                #print("post image method call")
                post = Post.objects.get(images_url__id=str(post_id))
                return post.images_url.get(id = post_id)
            except Post.DoesNotExist:
                return None
            

        elif post_type == PostType.VIDEO:
            try:
                #print("video  method call")
                post = Post.objects.get(id=post_id)
                return post
            except Post.DoesNotExist:
                return None
            
        else:
            return None
        
    def AddToPost(self, post) -> int:
        try:
            post.NoOflike = post.NoOflike+1
            post.update()
            return post.NoOflike
        except:
            pass
        try:
            post.noOfLike = post.noOfLike+1
            post.save()
            return post.noOfLike
        except:
            pass


    def MinusToPost(self, post):
        try:
            if post.NoOflike is 0:
                return post.NoOflike
            post.NoOflike = post.NoOflike-1
            post.update()
            return post.NoOflike
        except:
            pass
        try:
            if post.noOfLike is 0:
                return post.noOfLike
            post.noOfLike = post.noOfLike-1
            post.save()
            return post.noOfLike
        except:
            pass

    def post(self, request):
        user:AbstractBaseUser = request.user
        if user.is_authenticated:
            try:
                print(request.data)
                post_id = request.data['postId']
                post_type = request.data['postType']
                reactionType = request.data['reactionType']
                TYPE = request.data['type']
            except KeyError:
                err_403['message'] == "keyError"
                return Response(err_403)
            post = self.GetPostData(post_id, post_type)
            if post == None:
                err_404['message'] == "not found"
                return Response(err_404)
            try:
                
                REACTYPE:ReactOrUnReact = ReactOrUnReact(TYPE)
                if REACTYPE is ReactOrUnReact.REACT:
                    reaction:PostReactionType = PostReactionType(reactionType)
            except ValueError as e:
                text = {
                    "status":False,
                    "status_code":403,
                    "message": str(e)
                }
                print(text)
                return Response(text)
            
            if REACTYPE is ReactOrUnReact.REACT:
                like_filter = LikePost.objects.filter(post_id=post.id, username=user).first()
                rType:LikePost.ReactionType = self.getReactionType(reaction)
                if like_filter == None:
                    new_like = LikePost.objects.create(post_id=post.id, username=user, reactionType = rType)
                    new_like.save()
                    newLikeNumber = self.AddToPost(post=post)
                    if post_type != PostType.NEWSPOST:
                        LikeNotificationView.saveLike(ako=user, postId=post.id)
                    text = {
                        'status': True,
                        'message': 'post reacted',
                        'reaction': reactionType,
                        'post_likes': newLikeNumber}
                    print(text)
                    return Response(text)
                else:
                    like_filter.reactionType = rType
                    like_filter.save()
                    if post_type != PostType.NEWSPOST:
                        LikeNotificationView.saveLike(ako=user, postId=post.id)
                    try:
                        new_number_of_like = post.NoOflike
                    except:
                        new_number_of_like = post.noOfLike
                    text = {
                        'status': True,
                        'message': 'post reacted',
                        'reaction': reactionType,
                        'post_likes': new_number_of_like}
                    print(text)
                    return Response(text)
                
            elif REACTYPE is ReactOrUnReact.UNREACT:
                print(f"unreact {post}")
                like_to_delete = LikePost.objects.filter(post_id=post.id, username=user).first()
                if like_to_delete:
                    like_to_delete.delete()
                newLikeNumber = self.MinusToPost(post=post)
                if post_type is not PostType.NEWSPOST:
                    LikeNotificationView.deleteNotification(ako=request.user, postId=post.id)
                text = {
                    'status': True,
                    'message': 'post unReacted',
                    'reaction': None,
                    'post_likes': newLikeNumber}
                print(text)
                return Response(text)
            
    def getReactionType(self, reaction:PostReactionType) -> LikePost.ReactionType:
        if reaction == PostReactionType.LIKE:
            return LikePost.ReactionType.LIKE
        elif reaction == PostReactionType.LOVE:
            return LikePost.ReactionType.LOVE
        elif reaction == PostReactionType.HAPPY:
            return LikePost.ReactionType.HAPPY
        elif reaction == PostReactionType.WOW:
            return LikePost.ReactionType.WOW
        elif reaction == PostReactionType.SAD:
            return LikePost.ReactionType.SAD
        elif reaction == PostReactionType.ANGRY:
            return LikePost.ReactionType.ANGRY
            
class MyPostListView(APIView):
    data = {'status_code': 200, 'status': True, 'message': 'success'}
    success = {'status': True,'status_code': 200, 'message': 'success'}
    err = {"status":False, "message":"invalid token", "status_code":401}
    def get(self, request, page):
        user:AbstractBaseUser = request.user
        if user.is_authenticated:
            me = ProfileSerializer(Profile.objects.get(user = request.user))
            post_list = Post.objects.filter(Q(creator=user, media_type = 1) | Q(creator=user, media_type = 2) | Q(creator=user, media_type = 3) | Q(creator=user, media_type = 4))
            limit = page*16
            serializer = PostSerializer(post_list[int(limit)-16:int(limit)], many = True)
            for i in serializer.data:
                if len(i['image_url']) == 0 and len(i['videos_url']) == 1:
                    i['media_type'] = 6
                    i['videos'] = i['videos_url'][0]['url_w500']
                    i['url_w1000'] = i['videos_url'][0]['url_w1000']
                    i['url_w250'] = i['videos_url'][0]['url_w250']
                    i['playback_url'] = i['videos_url'][0]['playback_url']
                    i['thumbnail'] = i['videos_url'][0]['thumbnail']
                    i['width'] = i['videos_url'][0]['width']
                    i['height'] = i['videos_url'][0]['height']
                    del i['image_url']
                    del i['videos_url']

                i['creator_avatar'] = getAvatarByUsername(i['creator'])
                i['your_avatar'] = me.data['profileimg']
                i['dateCreated'] = i['created_at']
                i['created_at'] = getStringTime(i['created_at'])
                i['me'] = True if i['creator'] == request.user.username else False
                if LikePost.objects.filter(post_id=i['id'], username=request.user).exists():
                    i['is_like'] = True
                    i['reactionType'] = LikesPostSerializer(LikePost.objects.get(post_id=i['id'], username=request.user)).data['reactionType']
                else:
                    i['is_like'] = False
            if len(serializer.data) == 16:
                self.data['nextPageKey'] = page+1
                self.data['hasMorePage'] = True
                self.data['data'] = serializer.data
                return JsonResponse(self.data)
            else:
                self.data['hasMorePage'] = False
                self.data['nextPageKey'] = 1
                self.data['data'] = serializer.data
                return JsonResponse(self.data)
        return JsonResponse(self.err)
def getUser(user):
    try:
        a = User.objects.get(id = user)
        return a
    except:
        pass
    try:
        a = User.objects.get(username = user)
        return a
    except:
        pass
    try:
        a = User.objects.get(email = user)
        return a
    except:
        pass

    return None

class PostView(APIView):
    def get(self, request, user, page):
        if request.user.is_authenticated:
            me = ProfileSerializer(Profile.objects.get(user = request.user))
            page = page*16
            usr = getUser(user=user)
            if usr == None:
                err_404['message'] = "user not exists"
                return Response(err_404)
            post = Post.objects.filter(Q(creator = usr, privacy = "P") | Q(creator = usr, privacy = "F")).order_by("-created_at")

            serializer = PostSerializer(post[int(page)-16: int(page)], many = True)
            for i in serializer.data:
                i['creator_avatar'] = getAvatarByUsername(i['creator'])
                i['your_avatar'] = me.data['profileimg']
                i['dateCreated'] = i['created_at']
                i['created_at'] = getStringTime(i['created_at'])
                if LikePost.objects.filter(post_id=i['id'], username=request.user).exists():
                    i['is_like'] = True
                    i['reactionType'] = LikesPostSerializer(LikePost.objects.get(post_id=i['id'], username=request.user)).data['reactionType']
                else:
                    i['is_like'] = False
            success['message'] = "success"
            success['data'] = serializer.data
            return Response(success)

        err_401['message'] = "invalid user"
        return Response(err_401)
    err_404['message'] = "method not allowed"
    Response(err_404)

    
class MyGallery(APIView):
    def get(self, request, page):
        user = request.user
        if user.is_authenticated:
            post_list = Post.objects.filter(creator=user).order_by("created_at")
            limit = page*16
            imagelist=[]
            for post_images in post_list:
                imagelist.extend(post_images.images_url.all())
            serializer = ImagesSerializer(imagelist[int(limit)-16:int(limit)], many = True)
            for i in serializer.data:
                if LikePost.objects.filter(post_id=i['id'], username=request.user).exists():
                    i['is_like'] = True
                    i['reactionType'] = LikesPostSerializer(LikePost.objects.get(post_id=i['id'], username=request.user)).data['reactionType']
                else:
                    i['is_like'] = False
            if len(serializer.data) == 16:
                hasMorePage = True
            else:
                hasMorePage = False
            return Response({'status': True,
                             'status_code': 200,
                             'message': 'success',
                             'lenght': len(serializer.data),
                             'hasMorePage': hasMorePage,
                             'data': serializer.data
                             })
        return Response({"status":False,
                        "message":"invalid token",
                        "status_code":401,
                        "data": []
                        })
class DeleteCommentView(APIView):
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
        try:
            post = News.objects.get(id = str(post_id))
            return post
        except:
            pass
        return None
    def get(self, request, id, postId):
        if request.user.is_authenticated:
            user:AbstractBaseUser = request.user
            try:
                comment:Comment = Comment.objects.get(id = id, user = user)
                post = self.getPostData(post_id=postId)
            except Comment.DoesNotExist:
                err_404['message'] = "invalid data"
                return Response(err_404)
            comment.comment_type = 3
            comment.comments = None
            comment.isDeleted = True
            for i in comment.image.all():
                i.delete()
            for i in comment.video.all():
                i.delete()
            comment.save()
            if post.NoOfcomment != 0:
                post.NoOfcomment = post.NoOfcomment-1
            post.save()
            self.sendGroup(user=request.user, postId=postId, id=id)
            success['message'] = 'comment deleted'
            return Response(success)
        err_401['message'] = 'invalid user'
        return Response(err_401)
    
    def sendGroup(self, user:AbstractBaseUser, postId:str, id:str):
        channel_layer = get_channel_layer()
        group_name = postId
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "user":user.username,
                "data_type": 7,
                "commentId": str(id),
                "type":"new_comment_deleted"
            })
        return
    
class LikeComment(APIView):
    def sendToRoom(
        self, room:str, commentId:str,
        reactionType:PostReactionType,
        user:AbstractBaseUser,
        dataType:CommentTypes,
        NewLikeNumber:int,
        method:str,
        ):
        channel_layer = get_channel_layer()
        group_name = room
        async_to_sync(channel_layer.group_send)(
            group_name,
            {   "newLikeNumber": NewLikeNumber,
                "user":user.username,
                "reactionType":reactionType,
                "data_type": dataType,
                "commentId": str(commentId),
                "type":str(method)
            })
        return
    def GetPostData(self, post_id, post_type):
        if post_type == PostType.POST:
            try:
                #print("Post method call")
                post = Post.objects.get(id=post_id)
                return post
            except Post.DoesNotExist:
                return None
            
        elif post_type == PostType.NEWSPOST:
            try:
                #print("news post method call")
                post =  News.objects.get(id = post_id)
                return post
            except News.DoesNotExist:
                return None
            
        elif post_type == PostType.POSTIMAGE:
            try:
                #print("post image method call")
                post = Post.objects.get(images_url__id=str(post_id))
                return post.images_url.get(id = post_id)
            except Post.DoesNotExist:
                return None
            

        elif post_type == PostType.VIDEO:
            try:
                #print("video  method call")
                post = Post.objects.get(id=post_id)
                return post
            except Post.DoesNotExist:
                return None
            
        else:
            return None
    def post(self, request):
        user:AbstractBaseUser = request.user
        if user.is_authenticated:
            try:
                print(request.data)
                post_id = request.data['postId']
                comment_id = request.data['commentId']
                post_type = request.data['postType']
                reactionType = request.data['reactionType']
                TYPE = request.data['type']
            except KeyError:
                err_403['message'] == "keyError"
                return Response(err_403)
            try:
                commentToReact = Comment.objects.get(id = comment_id)
            except Comment.DoesNotExist:
                return Response({
                    'status': False,
                    'status_code': 404,
                    'message': 'comment not found'
                })
            post = self.GetPostData(post_id, post_type)
            if post == None:
                err_404['message'] == "not found"
                return Response(err_404)
            try:
                
                REACTYPE:ReactOrUnReact = ReactOrUnReact(TYPE)
                if REACTYPE is ReactOrUnReact.REACT:
                    reaction:PostReactionType = PostReactionType(reactionType)
            except ValueError as e:
                text = {
                    "status":False,
                    "status_code":403,
                    "message": str(e)
                }
                print(text)
                return Response(text)
            
            if REACTYPE is ReactOrUnReact.REACT:
                like_filter = Like_Comment.objects.filter(commentId = comment_id, user = user).first()
                rType:LikePost.ReactionType = self.getReactionType(reaction)
                if like_filter == None:
                    Like_Comment.objects.create(user = user, commentId=comment_id, reactionType = rType).save()
                    commentToReact.NoOflike+=1
                    commentToReact.save()
                    if post_type != PostType.NEWSPOST:
                        CommentNotificationView.Notify(post_id=post.id, request=request)
                    self.sendToRoom(
                        room=post.id,
                        commentId=comment_id,
                        reactionType=reaction,
                        user=user,
                        dataType=CommentTypes.CommentReacted,
                        NewLikeNumber=newLikeNumber,
                        method="new_comment_reacted"
                        )
                    text = {
                        'status': True,
                        'message': 'comment_reacted',
                        'reaction': reaction,
                        'commentLike': commentToReact.NoOflike}
                    print(text)
                    return Response(text)
                else:
                    like_filter.reactionType = rType
                    like_filter.save()
                    if post_type != PostType.NEWSPOST:
                        #CommentNotificationView.Notify(post_id=post.id, request=request)
                        pass
                    self.sendToRoom(
                        room=post.id,
                        commentId=comment_id,
                        reactionType=reaction,
                        user=user,
                        dataType=CommentTypes.CommentReacted,
                        NewLikeNumber=newLikeNumber,
                        method="new_comment_changeReaction"
                        )
                    new_number_of_like = commentToReact.NoOflike
                    text = {
                        'status': True,
                        'message': 'comment_reacted',
                        'reaction': reaction,
                        'commentLike': new_number_of_like}
                    print(text)
                    return Response(text)
                
            elif REACTYPE is ReactOrUnReact.UNREACT:
                print(f"unreact {post}")
                rType:Like_Comment.ReactionType = self.getReactionType(reaction)
                like_to_delete = Like_Comment.objects.filter(commentId = comment_id, user = user).first()
                if like_to_delete:
                    like_to_delete.delete()
                commentToReact.NoOflike -=1
                newLikeNumber = commentToReact.NoOflike
                if post_type is not PostType.NEWSPOST:
                    pass
                self.sendToRoom(
                    room=post.id,
                    commentId=comment_id,
                    reactionType=reaction,
                    user=user,
                    dataType=CommentTypes.CommentUnReacted,
                    NewLikeNumber=newLikeNumber,
                    method="new_comment_unreacted"
                    )
                text = {
                    'status': True,
                    'message': 'comment_unReacted',
                    'reaction': None,
                    'commentLike': newLikeNumber}
                print(text)
                return Response(text)
            
    def getReactionType(self, reaction:PostReactionType) -> Like_Comment.ReactionType:
        if reaction == PostReactionType.LIKE:
            return Like_Comment.ReactionType.LIKE
        elif reaction == PostReactionType.LOVE:
            return Like_Comment.ReactionType.LOVE
        elif reaction == PostReactionType.HAPPY:
            return Like_Comment.ReactionType.HAPPY
        elif reaction == PostReactionType.WOW:
            return Like_Comment.ReactionType.WOW
        elif reaction == PostReactionType.SAD:
            return Like_Comment.ReactionType.SAD
        elif reaction == PostReactionType.ANGRY:
            return Like_Comment.ReactionType.ANGRY

