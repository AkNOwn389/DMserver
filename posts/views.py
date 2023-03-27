
from .serializers import PostSerializer
from django.contrib.auth.models import User
from posts.models import Post, LikePost
from profiles.models import  Profile
from users.models import FollowerCount
from profiles.views import getAvatarByUsername
from time_.get_time import getStringTime
from profiles.serializers import ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from notifications.models import MyNotification
from .serializers import ImagesSerializer, PostUploader, PostCommentSerializer
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
    def Notify(self, creator_post_id, user):
        creator = User.objects.get(username = Post.objects.get(id = creator_post_id).creator)
        if not MyNotification.objects.filter(subject_id = creator_post_id, title = "Like your posts", subjectUser = user).first():
            MyNotification.objects.create(user = creator, subjectUser = user, subject_id = creator_post_id, title = "Like your posts", description = "", notifType = 2).save()
        return
    def deleteNotif(self, creator_post_id, user):
        creator = User.objects.get(username = Post.objects.get(id = creator_post_id).creator)
        try:
            MyNotification.objects.get(user = creator, subjectUser = user, subject_id = creator_post_id, title = "Like your posts", description = "", notifType = 2).delete()
        except MyNotification.DoesNotExist:
            pass

        return 
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
                self.Notify(creator_post_id=post_id, user=request.user)
                return JsonResponse({
                    'status': True,
                    'message': 'post like',
                    'post_likes': post.NoOflike})
            else:
                like_filter.delete()
                post.NoOflike = post.NoOflike-1
                post.save()
                self.deleteNotif(creator_post_id=post_id, user=request.user)
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
            print(serializer.data)
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
    
class CommentView(APIView):
    success = {'status': True, 'status_code': 200, 'message': 'success'}
    error_validation = {'status': False, 'status_code': 200, 'message': 'validation error'}
    err_not_exists = {'status': False, 'status_code': 200, 'message': 'post doest not exists'}

    def Notify(self, post_id, request):
        name = Profile.objects.get(user = request.user).name
        if name == "" or name == None:
            name = request.user.username
        creator = User.objects.get(username = Post.objects.get(id = post_id).creator)
        if creator == request.user:
            return
        MyNotification.objects.create(user = creator, subjectUser = request.user, subject_id = post_id, title = f"{name} commented on your posts", description = "", notifType = 3).save()
        return


    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            user_profile = Profile.objects.get(user = user)
            comment = request.data['comment']
            post_id = request.data['post_id']
            try:
                post = Post.objects.get(id = post_id)
            except Post.DoesNotExist:
                return JsonResponse(self.err_not_exists)

            a = Comment.objects.create(post_id = post_id, avatar = user_profile.profileimg, comments = comment, user = user)
            a.save()
            post.NoOfcomment = post.NoOfcomment+1
            post.save()
            self.Notify(post_id=post_id, request=request)
            return JsonResponse(self.success)

        return JsonResponse(self.error_validation)
