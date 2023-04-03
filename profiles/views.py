from posts.models import Post
from profiles.models import Profile
from users.models import FollowerCount
from users.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import ProfileSerializer
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.response import Response

# Create your views here.

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

def getAvatarByUsername(username):
    a = User.objects.get(username = username)
    b = Profile.objects.get(user = a)
    c = ProfileSerializer(b)
    return c.data['profileimg']
def getUserDataByUser(username):
    try:
        a = User.objects.get(username = username)
        b = Profile.objects.get(user = a)
    except User.DoesNotExist:
        return None
    except Profile.DoesNotExist:
        return None
    c = UserSerializer(a)
    e = ProfileSerializer(b)
    f = {**c.data, **e.data}
    return f

    


class search(APIView):
    def finder(self, user):
        search = str(user).replace("%20", " ").split(" ")
        print(search)
        users = []
        for posible in search:
            if posible == "":
                continue
            data = User.objects.filter(Q(username__contains = posible) | Q(first_name__contains = posible) | Q(last_name__contains = posible) | Q(email__contains = posible) | Q(first_name__contains =  str(posible).lower()) | Q(last_name__contains =  str(posible).lower()) | Q(username__contains = str(posible).lower()) | Q(email__contains = str(posible).lower() ))
            for i in data:
                if i not in users:
                    users.append(i)
        return users
    def get(self, request, user, page):
        if request.user.is_authenticated:
            page = page*16
            object = self.finder(user=user)
            data = []
            if len(object) != 0:
                data = []
                for ids in object:
                    if ids == request.user:
                        continue
                    usr = getUserDataByUser(ids)
                    if usr is not None:
                        data.append(usr)
                if len(data) == 16:
                    hasMorePage = True
                else:
                    hasMorePage = False
                success['message'] = 'User List Retreave'
                success['hasMorePage'] = hasMorePage
                success['data'] = data[page-16:page]
                return JsonResponse(success)
            success['status'] = False
            success['message'] = 'User List Retreave'
            success['data'] = []
            return Response(success)
        err_401['message'] = "user not logged"
        return Response(err_401)
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
            return Response({'status_code': 200,'status': True,'message': 'success','data': data})
        err_401['message'] = "user not logged"
        return Response(err_401)

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
            success['message'] = "success"
            success['data'] = data
            return Response(success)
        err_401['message'] = 'user not logged'
        return Response(err_401)



class UpdateDetails(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            try:
                user = Profile.objects.get(user = request.user)
                user.name = request.data['name']
                user.bio = request.data['bio']
                user.location = request.data['location']
                user.save()
                success['message'] = 'details update'
                return Response(success)
            except KeyError:
                err_404['message'] = "KeyError"
                return Response(err_404)
        err_401['message'] = 'invalid user'
        return Response(err_401) 

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
        return Response(success)

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                img = request.FILES.get('image')
            except KeyError:
                err_404['message'] = 'image required'
                return Response(err_404)
            if request.FILES['image'] != None:
                editor = Profile.objects.get(user = request.user)
                editor.profileimg = img
                editor.save()
                #upload posts
                return self.upload_image(request)
            err_404['message'] = 'invalid data'
            return Response(err_404)
        err_401['message'] = "ivalid user"
        return Response(err_401)
        
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
        return Response(success)

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                img = request.FILES.get('image')
            except KeyError:
                err_404['message'] = 'image required'
                return Response(err_404)
            if request.FILES['image'] != None:
                editor = Profile.objects.get(user = request.user)
                editor.bgimg = img
                editor.save()
                #upload posts
                return self.upload_image(request)
            err_404['message'] = 'invalid data'
            return Response(err_404)
        err_401['message'] = "ivalid user"
        return Response(err_401)
        
class avatarView(APIView):
    def get(self, request, user):
        me = request.user
        if me.is_authenticated:
            user_request = User.objects.get(username = user)
            if user_request is None:
                success['status'] = False
                success['message'] = 'user doests not exists'
                success['avatar'] = None
                return Response(success)
            she = Profile.objects.filter(user = user_request).first()
            she = ProfileSerializer(she)
            success['message'] = 'user doests not exists'
            success['avatar'] = she.data['profileimg']
            success['username'] = user_request.username
            success['name'] = she.data['name']
            success['message'] = 'success'
            return Response(success)
        err_401['message'] = "ivalid user"
        return Response(err_401)