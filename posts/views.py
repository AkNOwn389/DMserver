
from .serializers import PostSerializer
from django.contrib.auth.models import User
from posts.models import Post, LikePost
from profiles.models import  Profile
from users.models import FollowerCount
from profiles.views import getAvatarByUsername
from time_.get_time import getStringTime
from profiles.serializers import ProfileSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from .serializers import ImagesSerializer, PostUploader, PostCommentSerializer
from .models import Comment

# Create your views here.
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
                return JsonResponse({
                    'status': True,
                    'message': 'post like',
                    'post_likes': post.NoOflike})
            else:
                like_filter.delete()
                post.NoOflike = post.NoOflike-1
                post.save()
                return JsonResponse({
                    'status': True,
                    'message': 'post unlike',
                    'post_likes': post.NoOflike})
            
class get_post_list(APIView):
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
            self.success['data'] = serializer.data
            return JsonResponse(self.success)
        return JsonResponse(self.err)
    
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
            return JsonResponse(self.success)

        return JsonResponse(self.error_validation)
