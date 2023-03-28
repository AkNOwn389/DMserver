
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
from .models import Comment

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

class upload(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            isError = False
            try:
                images= request.FILES.getlist('image',)
            except KeyError:
                return JsonResponse({"status": False, 'status_code': 400, 'message': 'image required'})
            user = request.user
            data1 = request.data
            user_profile = Profile.objects.get(user = user)
            
            for i in images:
                y = {"image": i}
                x = ImagesSerializer(data = y)
                if x.is_valid(raise_exception=True):
                    pass
                else:
                    isError = True
            data2 = {'creator': user.id, 'creator_full_name': user_profile.name, 'description': data1['caption'], 'media_type': data1['media_type'], 'image_urls': images}
            serializer = PostUploader(data = data2)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                post = Post.objects.get(id = serializer.data['id'])
                if not isError:
                    for i in images:
                        post.images_url.create(image = i)
                    post.save()
                    return JsonResponse({'status': True,'status_code': 200, 'message': 'upload data success'})
                else:
                    post.delete()
                    return JsonResponse({'status': False,'status_code': 200, 'message': 'error'})
            else:
                return JsonResponse({'status': False,'status_code': 200, 'message': 'invalid data'})
            
        return JsonResponse({'status': False, 'status_code': 401, 'message': 'invalid user'})
    

class uploadTextPost(APIView):
    def post(self, request):
        me = request.user
        if me.is_authenticated:
            try:
                user = Profile.objects.get(user=request.user)
                data = {"creator": request.user.id, 'creator_full_name': user.name, "description": request.data['caption'], 'media_type': 1}
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
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            post_id = request.data['post_id']
            post = Post.objects.get(id=post_id)
            like_filter = LikePost.objects.filter(post_id=post_id, username=user).first()

            if like_filter == None:
                new_like = LikePost.objects.create(post_id=post_id, username=user)
                new_like.save()
                post.NoOflike = post.NoOflike+1
                post.save()
                LikeNotificationView.saveLike(ako=request.user, postId=post_id)
                return JsonResponse({
                    'status': True,
                    'message': 'post like',
                    'post_likes': post.NoOflike})
            else:
                like_filter.delete()
                post.NoOflike = post.NoOflike-1
                post.save()
                LikeNotificationView.deleteNotification(ako=request.user, postId=post_id)
                return JsonResponse({
                    'status': True,
                    'message': 'post unlike',
                    'post_likes': post.NoOflike})
            
class MyPostListView(APIView):
    success = {'status': True,'status_code': 200, 'message': 'beta test'}
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
            post = Post.objects.filter(creator = usr).order_by("-created_at")

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
            post_list = Post.objects.filter(creator=user)
            limit = page*16
            imagelist=[]
            for post_images in post_list:
                imagelist.extend(post_images.images_url.all())
            serializer = ImagesSerializer(imagelist[int(limit)-16:int(limit)], many = True)
            if len(serializer.data) < 16:
                hasMorePage = False
            else:
                hasMorePage = True
            return JsonResponse({'status': True,'status_code': 200, 'message': 'success','lenght': len(serializer.data), 'hasMorePage': hasMorePage, 'data': serializer.data})
        return JsonResponse({"status":False,
                             "message":"invalid token",
                             "status_code":401,
                             "data": []})
class DeleteCommentView(APIView):
    def get(self, request, id, postId):
        if request.user.is_authenticated:
            try:
                comment = Comment.objects.get(id = id, user = request.user)
                post = Post.objects.get(id = postId)
            except Comment.DoesNotExist:
                err_404['message'] = "invalid data"
                return Response(err_404)
            comment.delete()
            post.NoOfcomment = post.NoOfcomment-1
            print(post.NoOfcomment)
            post.save()
            success['message'] = 'comment deleted'
            return Response(success)
        err_401['message'] = 'invalid user'
        return Response(err_401)


class CommentView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            user_profile = Profile.objects.get(user = user)
            comment = request.data['comment']
            post_id = request.data['post_id']
            try:
                post = Post.objects.get(id = post_id)
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
                success['message'] = 'success'
                success['data'] = serializer.data
                success['data']['user_full_name'] = Profile.objects.get(user = User.objects.get(username = serializer.data['user'])).name
                success['data']['Followed'] = isFollowed(request.user, serializer.data['user'])
                success['data']['Follower'] = isFollower(request.user, serializer.data['user'])
                success['data']['created'] = getStringTime(serializer.data['created'])
                success['data']['me'] = True
                return JsonResponse(success)
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
                return Response(success)
            serialiser = PostCommentSerializer(comment[int(page)-16:int(page)], many = True)
            for i in serialiser.data:
                i['user_full_name'] = Profile.objects.get(user = User.objects.get(username = i['user'])).name
                i['Followed'] = isFollowed(request.user, i['user'])
                i['Follower'] = isFollower(request.user, i['user'])
                i['created'] = getStringTime(i['created'])
                i['me'] = True if i['user'] == request.user.username else False
            success['message'] = 'success'
            success['hasMorePage'] = True if len(serialiser.data) == 16 else False
            success['data'] = serialiser.data
            return Response(success)
        
        err_401['message'] = 'invalid user'
        return Response(err_401)
