
from .serializers import PostSerializer
from django.contrib.auth.models import User
from posts.models import Post, LikePost
from profiles.models import  Profile
from users.models import FollowerCount
from profiles.views import getAvatarByUsername
from time_.get_time import getStringTime
from users.views import isFollowed, isFollower
from profiles.serializers import ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from notifications.models import MyNotification
from .serializers import ImagesSerializer, PostUploader, PostCommentSerializer
from notifications.views import LikeNotificationView, CommentNotificationView
from .models import Comment, LikeComment as Like_Comment , Image as PostImage, Videos as PostVideos
from django.db.models import Q, F
from PIL import Image as ImagePIL, ImageFile
from django.db import transaction
from io import BytesIO, StringIO
from django.core.files import File
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO

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
                    img.delete()
                for i in posts.videos_url.all():
                    img = PostVideos.objects.get(id = str(i))
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
            for i in success['data']['image_url']:
                i['is_like'] = True if LikePost.objects.filter(post_id=i['id'], username=request.user).first() else False
            for i in success['data']['videos_url']:
                i['is_like'] = True if LikePost.objects.filter(post_id=i['id'], username=request.user).first() else False
            return Response(success)

#@transaction.atomic
class upload(APIView):
    def getType(self, request):
        print(request.data)
        try:
            images= request.FILES.getlist('image',)
        except Exception as e:
            images = None
            TYPE = 5
        try:
            videos = request.FILES.getlist('video',)
            return images, videos, 5
        except Exception as e:
            videos = None
            TYPE = 2
        if images == None and videos == None:
            TYPE = 0
        return images, videos, TYPE
    def put(self, request):
        if request.user.is_authenticated:
            isError = False
            images, videos, TYPE = self.getType(request=request)
            
            if images == None and videos == None:
                return Response({
                        'status': False,
                        'status_code': 403,
                        'message': 'media type not supported'
                    })
            user = request.user
            data = request.data
            user_profile = Profile.objects.get(user = user)
            
            for i in images:
                y = {"image": i}
                x = ImagesSerializer(data = y)
                if x.is_valid(raise_exception=True):
                    pass
                else:
                    isError = True
                    
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
                    if TYPE or TYPE == 5:
                        for i in images:
                            print(i)
                            postToUpload.images_url.create(image = i)
                        for i in postToUpload.images_url.all():
                            im = ImagePIL.open(i.image)
                            w, h = im.size
                            i.width = w
                            i.heigth = h
                            i.save()
                    if TYPE == 5:
                        for i in videos:
                            postToUpload.videos_url.create(videos = i)
                    postToUpload.save()
                except Exception as e:
                    print(e)
                    #postToUpload.delete()
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
    def GetPostData(self, post_id):
        try:
            post = Post.objects.get(id=post_id)
            return post, None
        except:
            pass
        try:
            post = Post.objects.get(images_url__id=str(post_id))
            return post.images_url.get(id = post_id), post
        except:
            pass

        return None, None
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            post_id = request.data['post_id']
            post, image_id = self.GetPostData(post_id)
            if post == None and image_id == None:
                err_404['message'] == "not found"
                return Response(err_404)
            

            like_filter = LikePost.objects.filter(post_id=post_id, username=user).first()

            if like_filter == None:
                new_like = LikePost.objects.create(post_id=post_id, username=user)
                new_like.save()
                post.NoOflike+=1
                post.save()
                if image_id != None:
                    post_id = image_id.id
                LikeNotificationView.saveLike(ako=request.user, postId=post_id)
                return JsonResponse({
                    'status': True,
                    'message': 'post like',
                    'post_likes': post.NoOflike})
            else:
                like_filter.delete()
                post.NoOflike-=1
                post.save()
                if image_id != None:
                    post_id = image_id.id
                #LikeNotificationView.deleteNotification(ako=request.user, postId=post_id)
                return JsonResponse({
                    'status': True,
                    'message': 'post unlike',
                    'post_likes': post.NoOflike})
            
class MyPostListView(APIView):
    success = {'status': True,'status_code': 200, 'message': 'success'}
    err = {"status":False, "message":"invalid token", "status_code":401}
    def get(self, request, page):
        user = request.user
        if user.is_authenticated:
            me = ProfileSerializer(Profile.objects.get(user = request.user))
            post_list = Post.objects.filter(creator=user)
            limit = page*16
            serializer = PostSerializer(post_list[int(limit)-16:int(limit)], many = True)
            for i in serializer.data:
                i['creator_avatar'] = getAvatarByUsername(i['creator'])
                i['your_avatar'] = me.data['profileimg']
                i['dateCreated'] = i['created_at']
                i['created_at'] = getStringTime(i['created_at'])
                if LikePost.objects.filter(post_id=i['id'], username=request.user).first():
                    i['is_like'] = True
                else:
                    i['is_like'] = False
            
            if len(serializer.data) == 16:
                hasMorePage = True
            else:
                hasMorePage = False
            self.success['hasMorePage'] = hasMorePage
            self.success['data'] = serializer.data
            return JsonResponse(self.success)
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
                if LikePost.objects.filter(post_id=i['id'], username=request.user).first():
                    i['is_like'] = True
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

        return None
    def get(self, request, id, postId):
        if request.user.is_authenticated:
            try:
                comment = Comment.objects.get(id = id, user = request.user)
                post = self.getPostData(post_id=postId)
            except Comment.DoesNotExist:
                err_404['message'] = "invalid data"
                return Response(err_404)
            comment.delete()
            post.NoOfcomment = post.NoOfcomment-1
            post.save()
            success['message'] = 'comment deleted'
            return Response(success)
        err_401['message'] = 'invalid user'
        return Response(err_401)

class LikeComments(APIView):
    def get(self, request, comment_id):
        if request.user.is_authenticated:
            try:
                coment = Comment.objects.get(id = comment_id)
            except Comment.DoesNotExist:
                return Response({
                    'status': False,
                    'status_code': 404,
                    'message': 'comment not found'
                })
            if Like_Comment.objects.filter(commentId = comment_id, user = request.user).first():
                Like_Comment.objects.get(commentId = comment_id, user = request.user).delete()
                coment.NoOflike-=1
                coment.save()
                return Response({
                    'status': True,
                    'status_code': 200,
                    'commentLike': coment.NoOflike,
                    'message': 'unlike'
                })

            else:
                Like_Comment.objects.create(user = request.user, commentId=comment_id).save()
                coment.NoOflike+=1
                coment.save()
                return Response({
                    'status': True,
                    'status_code': 200,
                    'commentLike': coment.NoOflike,
                    'message': 'like'
                })
        return Response({'status': False,
                         'status_code': 401,
                         'message': 'invalid user'})
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
            user = request.user
            user_profile = Profile.objects.get(user = user)
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
                a = Comment.objects.create(post_id = post_id, avatar = user_profile.profileimg, comments = comment, user = user, type = 1)
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
            comment = Comment.objects.filter(post_id = id).order_by("-created")
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
