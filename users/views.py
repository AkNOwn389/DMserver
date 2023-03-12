from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import FollowerCount
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from django.contrib.auth.models import User
from knox.auth import AuthToken
import random

# Create your views here.
def isFollowed(me, username):
    try:
        a = User.objects.get(username = username)
        b = FollowerCount.objects.get(user = a, follower = me)
        return True
    except:
        return False
def isFollower(me, username):
    try:
        a = User.objects.get(username = username)
        b = FollowerCount.objects.get(user = me, follower = a)
        return True
    except:
        return False

class WhoAmI(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return JsonResponse({"status":True,
                                 "status_code": 0,
                                "message":"ok",
                                "id":str(user.id),
                                "username": str(user.username)})
        else:
            return JsonResponse({"status":False,
                                 "status_code": 401,
                                "message":"ok",
                                "id": None,
                                "username": None})

class user_suggested(APIView):
    def get(self, request, page):
        if request.user.is_authenticated:
            page=page*16
            user_following = FollowerCount.objects.filter(follower=request.user)
            # user suggestion starts
            
            all_users = User.objects.all()
            user_following_all = []

            for user in user_following:
                user_list = User.objects.get(username=user.user)
                user_following_all.append(user_list)
            a = []
            new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
            current_user = User.objects.filter(username=request.user.username)
            admins = User.objects.filter(is_superuser = 1)
            a.extend(admins)
            a.extend(current_user)
            final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(a))]
            random.shuffle(final_suggestions_list)

            user_profile = []
            for users in final_suggestions_list[page-16:page]:
                profile_lists = Profile.objects.filter(user_id=users.id).first()
                serializer = ProfileSerializer(profile_lists)
                data = serializer.data
                user_profile.append(data)
            for i in user_profile:
                del i['bgimg']
                del i['bio']
                i['Followed'] = isFollowed(request.user, i['user'])
                i['Follower'] = isFollower(request.user, i['user'])
            return JsonResponse({'status': True, 'status_code': 200, 'data': user_profile})
        return JsonResponse({'status': 401,'message': 'user not logged'})

class get_follower(APIView):
    def get(self, request, page):
        if request.user.is_authenticated:
            user = request.user
            post_list = FollowerCount.objects.filter(user=user)
            limit = page*16
            follower = []
            if len(post_list) !=0:
                for x in post_list:
                    a = Profile.objects.get(user = x.follower)
                    follower.append(a)

                serializer = ProfileSerializer(follower[int(limit)-16:int(limit)], many = True)
                for i in serializer.data:
                    del i['bio']
                    del i['bgimg']
                    i['Followed'] = isFollowed(request.user, i['user'])
                    i['Follower'] = isFollower(request.user, i['user'])
                return JsonResponse({'status': True, 'status_code': 200, 'message': 'beta test', 'data': serializer.data})
            return JsonResponse({'status': True, 'status_code': 200, 'message': 'you have no followers at this time.', 'data': []})
        return JsonResponse({"status": False,"status_code":401,"message":"invalid user"})
    
class get_following_list(APIView):
    def get(self, request, page):
        if request.user.is_authenticated:
            user = request.user
            post_list = FollowerCount.objects.filter(follower=user)
            limit = page*16
            if len(post_list) != 0:
                following = []
                for x in post_list:
                    a = Profile.objects.get(user = x.user)
                    following.append(a)

                serializer = ProfileSerializer(following[int(limit)-16:int(limit)], many = True)
                for i in serializer.data:
                    del i['bio']
                    del i['bgimg']
                    i['Followed'] = isFollowed(request.user, i['user'])
                    i['Follower'] = isFollower(request.user, i['user'])
                return JsonResponse({'status': True, 'status_code': 200, 'message': 'success', 'data': serializer.data})
            return JsonResponse({'status': True, 'status_code': 200, 'message': 'you have no followed at this time.', 'data': []})
        return JsonResponse({"status": False,"status_code":401,"message":"invalid user"})
class get_friend(APIView):
    def get(self, request, page):
        if request.user.is_authenticated:
            limit = page*16
            friend = []
            following = FollowerCount.objects.filter(follower = request.user)
            if len(following) == 0:
                return JsonResponse({"status": True, 'status_code': 200, 'message': 'you have no friends at time.', 'data': []})
            for x in following:
                f2f = FollowerCount.objects.filter(user = request.user, follower = x.user).first()
                if f2f is not None:
                    friend.append(f2f)
            friends = []
            for user in friend:
                a = Profile.objects.get(user = user.follower)
                if a is not None:
                    friends.append(a)
            if len(friends) != 0:
                serializer = ProfileSerializer(friends[int(limit)-16:int(limit)], many = True)
                for i in serializer.data:
                    del i['bio']
                    del i['bgimg']
                return JsonResponse({"status": True, 'status_code': 200, "message": "success", "data": serializer.data})

            return JsonResponse({"status": True, 'status_code': 200, 'message': 'you have no friends at time.', 'data': []})
        return JsonResponse({"status": False,"status_code":401,"message":"invalid user"})

class logout(APIView):
    def get(self, request):
        key = request.headers['Authorization'].split()[1][:8]
        user = AuthToken.objects.get(token_key = key)
        if user is None:
            return JsonResponse({'status_code': 401, 'message': 'system failure'})
        user.delete()
        return JsonResponse({'status': True, 'message': 'user logged-out'})

    def post(self, request):
        user = User.objects.filter(username = request.user).first()
        if user is not None:
            if not user.check_password(request.data['password']):
                return Response({
                    'status': False,
                    'message': 'Invalid password'
                })
            user_token = AuthToken.objects.filter(user = request.user)
            user_token.delete()
            return JsonResponse({'status': True, 'message': 'all account logged-out'})
        
class login(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username = username).first()
        if user is None:
            user = User.objects.filter(email=username).first()
        if user is not None:
            user_profile = Profile.objects.filter(user = user).first()
            user_profile_serialize = ProfileSerializer(user_profile)
            if not user.check_password(password):
                return Response({
                    'status': False,
                    'status_code': 1,
                    'message': 'Invalid password'
                })
            #user, token = AuthToken.objects.create(user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': True,
                'status_code': 200,
                'message':'login success',
                'info': user_profile_serialize.data,
                'token': {
                    'refresh_token': str(refresh),
                    'tokenType': 'Bearer',
                    'accesstoken': str(refresh.access_token)
                    }})
            
        
        else:
            return Response({
                'staus': False,
                'status_code': 2,
                'message': 'User not exists'
            })
        
class signup(APIView):
    def post(self, request):
        username = request.data['username']
        email = request.data['email']
        name = request.data['name'].split()
        password = request.data['password']
        password2 = request.data['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                return JsonResponse({'status':False,'message': 'Email already exists'})
            elif User.objects.filter(username=username).exists():
                return JsonResponse({'status':False,'message': 'Username already exists'})
            else:
                if len(name) > 1:
                    user = User.objects.create_user(username=username, email=email, password=password, first_name = name[0], last_name = name[1])
                    user.save()
                else:
                    user = User.objects.create_user(username=username, email=email, password=password, first_name = name[0])
                    user.save()
                if len(name) > 1:
                    name = name[0]+' '+name[1]
                elif len(name) > 2:
                    name = name[0]+' '+name[1]+' '+name[2]
                else:
                    name = name[0]
                user_model = User.objects.get(username=username)
                _, token = AuthToken.objects.create(user_model)
                new_profile = Profile.objects.create(user=user_model, name=name)
                new_profile.save()
                user_profile = Profile.objects.filter(user = user).first()
                user_profile_serialize = ProfileSerializer(user_profile)
                return Response({
                    'status': True,
                    'message':'register success',
                    'status_code': 200,
                    'info': user_profile_serialize.data,
                    'token': {
                        'tokentype': 'token',
                        'accesstoken': token
                        }})
        else:
            return Response({
                'status': False,
                'message': 'Password not matches'
            })