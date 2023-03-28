from posts.models import Post
from profiles.models import Profile
from users.models import FollowerCount
from users.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import ProfileSerializer
from django.http import JsonResponse

# Create your views here.
def getAvatarByUsername(username):
    a = User.objects.get(username = username)
    b = Profile.objects.get(user = a)
    c = ProfileSerializer(b)
    return c.data['profileimg']
class search(APIView):
    def finder(self, user):
        x = User.objects.filter(username__contains = user)
        if len(x) == 0:
            x = User.objects.filter(first_name__contains = user)
            if len(x) == 0:
                x = User.objects.filter(last_name__contains = user)
                if len(x) == 0:
                    x = User.objects.filter(email__contains = user)
                    if len(x) == 0:
                        return x
                    else:
                        return x
                else:
                    return x
            else:
                return x
        else:
            return x
    def get(self, request, user, page):
        if request.user.is_authenticated:
            page = page*16
            object = self.finder(user=user)
            data = []
            if len(object) != 0:
                for ids in object:
                    profile_lists = Profile.objects.get(user_id=ids.id)
                    data.append(profile_lists)
                u = []
                v = []
                for i in range(len(data)):
                    x = UserSerializer(object[i])
                    z = ProfileSerializer(data[i])
                    u.append(x.data)
                    v.append(z.data)
                w = []
                for i in range(len(v)):
                    d = {**u[i], **v[i]}
                    w.append(d)
                if len(w) <= 16:
                    hasMorePage = False
                else:
                    hasMorePage = True
                return JsonResponse({'status': True, 'status_code': 200, 'message': 'User List Retreave', 'hasMorePage': hasMorePage, 'data': w[page-16:page]})
            return JsonResponse({'status': False, 'status_code': 200, 'message': 'User List Retreave', 'data': []})
        return JsonResponse({'status': 401,'message': 'user not logged'})
class Me(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            mydata = User.objects.filter(id=user.id).first()
            myprofile = Profile.objects.filter(user_id=user.id).first()
            mypost = Post.objects.filter(creator = user)
            user_followers = len(FollowerCount.objects.filter(user=request.user))
            user_following = len(FollowerCount.objects.filter(follower=request.user))
            serialize_data = UserSerializer(mydata)
            serialize_profile = ProfileSerializer(myprofile)
            data = {**serialize_data.data, **serialize_profile.data}
            data['followers'] = user_followers
            data['following'] = user_following
            data['post_lenght'] = len(mypost)
            return JsonResponse({'status_code': 200,'status': True,'message': 'success','data': data})
        return JsonResponse({'status_code': 401,'status': False, 'message': 'user not logged'})

class profile(APIView):
    def get(self, request, user):
        if request.user.is_authenticated:
            mydata = User.objects.get(username=user)
            myprofile = Profile.objects.get(user_id=mydata.id)
            mypost = Post.objects.filter(creator = mydata.id)
            user_followers = len(FollowerCount.objects.filter(user=mydata.id))
            user_following = len(FollowerCount.objects.filter(follower=mydata.id))
            serialize_data = UserSerializer(mydata)
            serialize_profile = ProfileSerializer(myprofile)
            data = {**serialize_data.data, **serialize_profile.data}
            data['followers'] = user_followers
            data['following'] = user_following
            data['post_lenght'] = len(mypost)
            data['isFollowing'] = True if FollowerCount.objects.filter(user = mydata, follower = request.user).first() else False
            data['isFollower'] = True if FollowerCount.objects.filter(follower = mydata, user = request.user).first() else False
            return JsonResponse({'status_code': 200,'status': True,'message': 'success','data': data})
        return JsonResponse({'status': 401,'message': 'user not logged'})



class UpdateDetails(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            try:
                user = Profile.objects.get(user = request.user)
                user.name = request.data['name']
                user.bio = request.data['bio']
                user.location = request.data['location']
                user.save()
                return JsonResponse({'status': True, 'status_code': 200, 'message': 'details update'})
            except KeyError:
                return JsonResponse({'status': False, 'status_code': 200, 'message': 'Key Error'})
        return JsonResponse({'status': False, 'status_code': 401, 'message': 'invalid user'}) 

class ProfilePictureUpdate(APIView):
    def upload_image(self, request):
        profile = Profile.objects.get(user = request.user)
        try:
            caption = request.data["caption"]
        except KeyError:
            caption = ""
        new_post = Post.objects.create(creator_full_name = profile.name, creator_id = request.user.id, description = caption, media_type = 3, title = "Update here profile picture")
        new_post.images_url.create(image = profile.profileimg)
        new_post.save()
        return JsonResponse({'status': True,'status_code': 200, 'message': 'upload success'})

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                img = request.FILES.get('image')
            except KeyError:
                return JsonResponse({"status": False, 'status_code': 200, 'message': 'image required'})
            if request.FILES['image'] != None:
                editor = Profile.objects.get(user = request.user)
                editor.profileimg = img
                editor.save()
                #upload posts
                return self.upload_image(request)
            return JsonResponse({'status': False,'status_code': 200, 'message': 'invalid data'})
        
class ProfileCoverUpdate(APIView):
    def upload_image(self, request):
        profile = Profile.objects.get(user = request.user)
        try:
            caption = request.data["caption"]
        except KeyError:
            caption = ""
        new_post = Post.objects.create(creator_full_name = profile.name, creator_id = request.user.id, description = caption, media_type = 4, title = "Update here cover photo")
        new_post.images_url.create(image = profile.bgimg)
        new_post.save()
        return JsonResponse({'status': True,'status_code': 200, 'message': 'upload success'})

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                img = request.FILES.get('image')
            except KeyError:
                return JsonResponse({"status": False, 'status_code': 200, 'message': 'image required'})
            if request.FILES['image'] != None:
                editor = Profile.objects.get(user = request.user)
                editor.bgimg = img
                editor.save()
                #upload posts
                return self.upload_image(request)
            return JsonResponse({'status': False,'status_code': 200, 'message': 'invalid data'})
        
class avatarView(APIView):
    def get(self, request, user):
        me = request.user
        if me.is_authenticated:
            user_request = User.objects.get(username = user)
            if user_request is None:
                return JsonResponse({'status': False,'status_code': 200, 'message': 'user doests not exists', 'avatar': None})
            she = Profile.objects.filter(user = user_request).first()
            she = ProfileSerializer(she)
            return JsonResponse({'status': True,'status_code': 200, 'message': 'success', 'avatar': str(she.data['profileimg']), 'username': user_request.username, 'name': str(she.data['name'])})
        return JsonResponse({"status": False,"status_code":401,"message":"invalid user"})