from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken
from Authentication.models import UserRegisterCode, UserRecoveryCode, RecoveryAccountSpecialId
from Authentication.serializers import UserRegisterCodeSerializer, UserRecoveryCodeSerializer, RecoverAccountSpecialIdSerializer
from users.models import FollowerCount
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import timedelta
from django.db.models.functions import Now
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser
from rest_framework_simplejwt.exceptions import TokenError
from notifications.views import FollowNotificationView
from django.db.models import Q
from .models import OnlineUser, ChangePasswordHistory
from .serializers import ChangePasswordHistorySerializer
from smtplib import SMTPRecipientsRefused
import random, uuid
from django.utils import timezone
from datetime import datetime
from django.http import HttpRequest
from .dbManager import sendRecoveryCodeEmailFromUser, sendEmailFromUser, get_client_ip
import time
from time_.get_time import getStringTime, getStringTimeForSwitchAccount


success = {"status": True, "status_code": 200}
err_400 = {"status": False, "status_code": 400}
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
# Create your views here.



def isFollowed(me:AbstractBaseUser, username) -> bool:
    try:
        a = User.objects.get(username = username)
        return FollowerCount.objects.filter(user = a, follower = me).exists()
    except:
        return False
def isFollower(me:AbstractBaseUser, username) -> bool:
    try:
        a = User.objects.get(username = username)
        return FollowerCount.objects.filter(user = me, follower = a).exists()
    except:
        return False
    
def isOnline(user=None, username = None) -> bool:
    if user == None:
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            return False
    elif username == None:
        return False
    
    if OnlineUser.objects.filter(user = user).first():
        return True
    else:
        return False

class changePasswordView(APIView):
    def post(self, request:HttpRequest):
        try:
            user:AbstractBaseUser = request.user
            if user.is_authenticated:
                oldPassword = request.data['oldPassword']
                newPassword = request.data['newPassword']
                retype = request.data['confirmNewPassword']
                device = request.data['device']
                ip = get_client_ip(request=request)
                userToChangePassword = User.objects.get(pk = user.pk)
                if str(oldPassword) == str(newPassword):
                    return Response({
                        "status": False,
                        "status_code": 403,
                        "message": "password are same."
                    })
                if userToChangePassword.check_password(oldPassword):
                    if str(newPassword) == str(retype):
                        data = {"ip": ip,
                                "device": device,
                                "user": userToChangePassword.pk}
                        serializer = ChangePasswordHistorySerializer(data=data)
                        if serializer.is_valid(raise_exception=True):
                            serializer.save()
                            userToChangePassword.set_password(newPassword)
                            userToChangePassword.save()
                            return Response({"status":True,
                                        "status_code": 200,
                                        "message": "success"})
                        else:
                            return Response({"status":False,
                                        "status_code": 403,
                                        "message": "invalid cridentials"})
                    else:
                        return Response({"status":False,
                                "status_code": 403,
                                "message": "password not match"})
                else:
                    return Response({"status":False,
                                "status_code": 403,
                                "message": "invalid password"})
            else:
                return Response({"status":False,
                                "status_code": 401,
                                "message": "invalid user"})
        except Exception as e:
            return Response({"status":False,
                            "status_code": 401,
                            "message":str(e),
                            "id": None,
                            "username": None})

class BahaviorLoginEvent(APIView):
    def get(self, request:HttpRequest):
        user:AbstractBaseUser = request.user
        try:
            if user.is_authenticated:
                usr = User.objects.get(pk = user.pk)
                usr.last_login = timezone.now()
                usr.save()
                return Response({"status":True,
                                    "status_code": 0,
                                    "message":"ok",
                                    "id":str(user.id),
                                    "username": str(user.username)})
            else:
                return Response({"status":False,
                                    "status_code": 401,
                                    "message":"ok",
                                    "id": None,
                                    "username": None})
        except Exception as e:
            print(e)
            return Response({"status":False,
                                    "status_code": 403,
                                    "message":str(e),
                                    "id": None,
                                    "username": None})

class user_suggested(APIView):
    def get(self, request:HttpRequest, page:int):
        if request.user.is_authenticated:
            page=page*16
            user_following = FollowerCount.objects.filter(Q(follower=request.user) | Q(user = request.user))
            
            # user suggestion starts
            
            all_users = User.objects.all()
            user_following_all = []

            for user in user_following:
                try:
                    user_list = User.objects.get(username=user.user)
                    if user_list.is_superuser or user_list.is_staff or user_list.is_anonymous:
                        continue
                    #if not user_list in user_following_all:
                    user_following_all.append(user_list)
                except User.DoesNotExist:
                    pass
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
                i['Following'] = isFollowed(request.user, i['user'])
                i['Follower'] = isFollower(request.user, i['user'])
            return Response({'status': True, 'status_code': 200, 'message': 'user list retrive', 'data': user_profile})
        return Response({'status': 401,'message': 'user not logged'})
class Follow(APIView):
    def get(self, request:HttpRequest, user:str):
        if request.user.is_authenticated:
            if request.user.username == user:
                return Response({"status":False, "status_code": 0, "message": "invalid data"})
            try:
                following = User.objects.get(username = user)
            except:
                return Response({'status': False, 'status_code':0, 'message': 'user not exists'})
            if FollowerCount.objects.filter(follower=request.user, user=following).first():
                delete_follower = FollowerCount.objects.get(follower=request.user, user=following)
                delete_follower.delete()
                FollowNotificationView.deleteNotif(request=request, following=following)
                return Response({'status':True,'status_code': 200, 'message': 'unfollowed'})
            else:
                new_follower = FollowerCount.objects.create(follower=request.user, user=following)
                new_follower.save()
                FollowNotificationView.Notify(request=request, following=following)
                return Response({'status':True, 'status_code': 200, 'message': 'following'})
        return Response({'status':False, 'status_code': 401, 'message': 'user not logged'})
    
class DeniedFollow(APIView):
    def get(self, request:HttpRequest, user:str):
        if request.user.is_authenticated:
            if request.user.username == user:
                return Response({
                    "status":False,
                    "status_code": 404,
                    "message": "invalid data"})
            try:
                usr = User.objects.get(username = user)
            except:
                return Response({
                    'status': False,
                    'status_code':404,
                    'message': 'user not exists'})
            
            try:
                f = FollowerCount.objects.get(follower = usr, user = request.user)
                f.delete()
                return Response({
                    'status': True,
                    'status_code': 200,
                    'message': 'success'
                })
            except FollowerCount.DoesNotExist:
                return Response({
                    'status': False,
                    'status_code': 404,
                    'message': 'request not exists'
                })
        return Response({
            'status':False,
            'status_code': 401,
            'message': 'user not logged'
            })
class get_follower(APIView):
    def get(self, request:HttpRequest, page:int):
        if request.user.is_authenticated:
            user = request.user
            usr = FollowerCount.objects.filter(user=user)
            limit = page*16
            follower = []
            if len(usr) !=0:

                for x in usr:
                    if FollowerCount.objects.filter(user = x.follower, follower = request.user).first():
                        continue
                    a = Profile.objects.get(user = x.follower)
                    follower.append(a)
                if len(follower) != 0:
                    serializer = ProfileSerializer(follower[int(limit)-16:int(limit)], many = True)
                    for i in serializer.data:
                        del i['bio']
                        del i['bgimg']
                        i['Following'] = isFollowed(request.user, i['user'])
                        i['Follower'] = isFollower(request.user, i['user'])
                    
                    return Response(status=200, data={
                        'status': True,
                        'status_code': 200,
                        'message': 'success',
                        'hasMorePage': True if len(serializer.data) == 16 else False,
                        'data': serializer.data
                    })
            
            return Response(status=200, data={
                'status': True,
                'status_code': 200,
                'message': 'you have no followers at this time.',
                'data': []
            })
        
        err_401['message'] = "invalid cridential"
        return Response(err_401)
    
class get_following_list(APIView):
    def get(self, request:HttpRequest, page:int):
        if request.user.is_authenticated:
            user = request.user
            post_list = FollowerCount.objects.filter(follower=user)
            limit = page*16
            if len(post_list) != 0:
                following = []
                for x in post_list:
                    if FollowerCount.objects.filter(user = request.user, follower = x.user).first():
                        continue
                    a = Profile.objects.get(user = x.user)
                    following.append(a)

                if len(following) != 0:
                    serializer = ProfileSerializer(following[int(limit)-16:int(limit)], many = True)
                    for i in serializer.data:
                        del i['bio']
                        del i['bgimg']
                        i['Followed'] = isFollowed(request.user, i['user'])
                        i['Follower'] = isFollower(request.user, i['user'])
                    return Response(status=200, data={
                            'status': True,
                            'status_code': 200,
                            'message': 'success',
                            'hasMorePage': True if len(serializer.data) == 16 else False,
                            'data': serializer.data
                        })
                

            return Response(status=200, data={
                'status': True,
                'status_code': 200,
                'message': 'you have no followed at this time.',
                'data': []
            })
            
        err_401['message'] = "invalid cridential"
        return Response(err_401)
class CancelRequest(APIView):
    def get(self, request:HttpRequest, user:str):
        if request.user.is_authenticated:
            try:
                usr = User.objects.get(username = user)
            except User.DoesNotExist:
                return Response({
                    'status': False,
                    'status_code': 404,
                    'message': 'user not found'
                })
            try:
                FollowerCount.objects.get(follower = request.user, user = usr).delete()
                return Response({
                    'status': True,
                    'status_code': 200,
                    'message': 'canceled'
                })
            
            except FollowerCount.DoesNotExist:
                return Response({
                    'status': False,
                    'status_code': 404,
                    'message': 'user not found'
                })
        return Response({
            'status': False,
            'status_code': 401,
            'message': 'user not logged'
        })

class IsAuthenticated(APIView):
    def get(self, request:HttpRequest):
        if request.user.is_authenticated:
            profile:Profile = Profile.objects.get(user = request.user)
            user:AbstractBaseUser = request.user
            return Response({
                'status': True,
                'status_code': 200,
                'message': 'success',
                'data':{
                    'username': user.username,
                    'id': user.pk,
                    'name': profile.name,
                }
            })
        else:
            return Response({
                'status': False,
                'status_code': 401,
                'message': 'invalid user',
            })
class RecoverAccountRequestOthenticationView(APIView):
    def post(self, request:HttpRequest):
        try:
            email = request.data['email']
        except:
            return Response({"status": False,
                             "status_code": 403,
                             "message": "email is required"
                             })
        if User.objects.filter(email = email).exists():
            id = uuid.uuid4()
            code = random.randint(100000, 999999)
            expiration = datetime.now()+timedelta(minutes=5)
            if UserRecoveryCode.objects.filter(email = email, expiration__gt = Now(), attempt = 5).exists():
                return Response({"status": False,
                                "status_code": 0,
                                "message": "max attempt reach please wait 5 minutes"
                                })
            elif UserRecoveryCode.objects.filter(email = email, expiration__gt = Now()).exists():
                current = UserRecoveryCode.objects.get(email = email, expiration__gt = Now())
                return Response({"status": False,
                                "status_code": 1,
                                "message": "already requested please wait 5 minutes",
                                "data": {
                                    'requestId': current.id, 
                                    'email': email}
                                })
            data = {"id": id, "email": email, "verificationCode": code, "expiration": str(expiration)}
            serialiser = UserRecoveryCodeSerializer(data = data)
            if serialiser.is_valid():
                if sendRecoveryCodeEmailFromUser(code=code, useremail=email):
                    serialiser.save()
                    return Response({"status": True, 
                                     "status_code": 200, 
                                     "message": "authentication created", 
                                     'data': {'requestId': id, 
                                              'email': email
                                              }
                                     })
                else:
                    return Response({
                        "status":False,
                        "status_code": 403,
                        "message": "system failure"
                    })
            return Response({
                        "status":False,
                        "status_code": 403,
                        "message": "cridential error"
                    })
        else:
            return Response({
                        "status":False,
                        "status_code": 403,
                        "message": "Can't find connected account in this email."
                    })
class RecoverAccountView(APIView):
    def put(self, request:HttpRequest):
        try:
            recoveryKey = request.data['recoveryKey']
            user:str = request.data['user']
            userId:str = request.data['userId']
            email:str = request.data['email']
            newPassword:str = request.data['newPassword']
            newPasswordConfirm:str = request.data['newPasswordConfirm']
        except:
            return Response({
                "status": False,
                "status_code": 403,
                "message": "missing credential"
            })
        
        if str(newPassword) != str(newPasswordConfirm):
            return Response({
                "status": False,
                "status_code": 403,
                "message": "password not matche"
            })
            
        if RecoveryAccountSpecialId.objects.filter(id = recoveryKey, accountToRecover = userId, email = email).exists():
            RecoveryAccountSpecialId.objects.get(id = recoveryKey, accountToRecover = userId, email = email).delete()
            user:AbstractBaseUser = User.objects.get(id = userId, username = user, email = email)
            user.set_password(newPassword)
            user.save()
            
            return Response({
                "status": True,
                "status_code": 200,
                "message": "success"
            })
            
        else:
            return Response({
                "status": False,
                "status_code": 403,
                "message": "invalid recovery key"
            })
        
    def post(self, request:HttpRequest):
        try:
            email:str = request.data['email']
            otpCode:str = request.data['code']
            recoveryCodeId:str = request.data['requestId']
        except:
            return Response({
                "status": False,
                "status_code": 403,
                "message": "missing credential"
            })
        if UserRecoveryCode.objects.filter(id = recoveryCodeId, expiration__gt = Now()).exists():
            registerCodeTable = UserRecoveryCode.objects.get(id = str(recoveryCodeId))
            if registerCodeTable.attempt >= 5:
                return Response({"status": False, 
                                 "status_code": 0,
                                 "remaining_attempt": 0,
                                 "message": "max attempt reach"
                                 })
            else:
                if str(registerCodeTable.verificationCode).strip() != str(otpCode).strip():
                    registerCodeTable.attempt += 1
                    registerCodeTable.save()
                    return Response({"status": False, 
                                    "status_code": 200,
                                    "remaining_attempt": 5-registerCodeTable.attempt,
                                    "message": "invalid code",
                                    })
                elif str(registerCodeTable.email).strip() != str(email).strip():
                    return Response({"status": False, 
                                    "status_code": 200,
                                    "remaining_attempt": 5-registerCodeTable.attempt,
                                    "message": "invalid recovery email"
                                    })
                else:
                    #Passes in security
                    user:AbstractBaseUser = User.objects.get(email = email)
                    specialKey:RecoveryAccountSpecialId = RecoveryAccountSpecialId.objects.create(accountToRecover = user, email = user.email)
                    specialKey.save()
                    text = {
                        "status": True,
                        "status_code": 200,
                        "message": "success",
                        "data": {
                            "max_password_change": 1,
                            "recoveryKey": specialKey.id,
                            "email": specialKey.email,
                            "user":  user.username,
                            "userId": user.pk,
                        }
                    }
                    print(text)
                    return Response(text)
        else:
            return Response({"status": False, 
                             "status_code": 1, 
                             "message": "Expired code",
                             "remaining_attempt": 0,
                             })

class GetUserData(APIView):
    def post(self, request:HttpRequest):
        if request.user.is_authenticated:
            user:AbstractBaseUser = request.user
            userToGet = request.data['username']
            print(userToGet)
            if User.objects.filter(username = userToGet).exists():
                user2:AbstractBaseUser = User.objects.get(username = userToGet)
                profile:dict = ProfileSerializer(Profile.objects.get(user = user2)).data
                text = {
                    'status': True,
                    'status_code': 200,
                    'message': 'success',
                    'username': str(user2.username),
                    'image': str(profile['profileimg']),
                    'id': str(user2.pk),
                    'name': str(profile['name']),
                    'lastLogin': str(user2.last_login),
                    'lastLoginDisplay': getStringTimeForSwitchAccount(user2.last_login)
                }
                print(text)
                return Response(text, status=200)
            else:
                return Response({
                    'status': False,
                    'status_code': 404,
                    'message': 'user not exists.'
                })
        else:
            return Response({
                'status': False,
                'status_code': 401,
                'message': 'invalid user',
            })

class get_friend(APIView):
    def get(self, request:HttpRequest, page:int):
        if request.user.is_authenticated:
            limit = page*16
            friend = []
            following = FollowerCount.objects.filter(follower = request.user)
            if len(following) == 0:
                return Response({
                    "status": True,
                    'status_code': 200,
                    'message': 'you have no friends at time.',
                    'data': []
                    })
            
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
                    i['Followed'] = isFollowed(request.user, i['user'])
                    i['Follower'] = isFollower(request.user, i['user'])

                return Response(status=200, data={
                            'status': True,
                            'status_code': 200,
                            'message': 'success',
                            'hasMorePage': True if len(serializer.data) == 16 else False,
                            'data': serializer.data
                        })


            return Response(status=200, data={
                'status': True,
                'status_code': 200,
                'message': 'you have no friends at time.',
                'data': []
            })
            
        err_401['message'] = "invalid cridential"
        return Response(err_401)

class logout(APIView):
    def post(self, request:HttpRequest):
        if request.user.is_authenticated:
            key = request.headers['Authorization'].split()[1]
            refresh = request.data['refresh_token']
            try:
                a = RefreshToken(refresh)
                a.blacklist()
            except TokenError:
                pass
            """
            print(key)
            token = jwt.decode(key, settings.SECRET_KEY, algorithms=[settings.ALGORITHYM])
            print(token)
            token_id = token['id']
            blacklistedtoken = BlacklistedToken.objects.create(token_id=token_id, blacklisted_at = timezone.now())
            blacklistedtoken.save()
            """
            return Response({'status': True, 'message': 'user logged-out'})
class logoutAll(APIView):
    def post(self, request:HttpRequest):
        if request.user.is_authenticated:
            user = User.objects.filter(username = request.user).first()
            if user is not None:
                if not user.check_password(request.data['password']):
                    return Response({
                        'status': False,
                        'message': 'Invalid password'
                    })
                a = OutstandingToken.objects.filter(user_id = user.id)
                for token in a:
                    blacklistedtoken = BlacklistedToken.objects.create(token_id=token.id, blacklisted_at = timezone.now())
                    blacklistedtoken.save()
                
                return Response({'status': True, 'message': 'all account logged-out'})
        
class login(APIView):
    def post(self, request:HttpRequest):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username = username).first()
        if user is None:
            user = User.objects.filter(email=username).first()
        if user is not None:
            if user.is_superuser or user.is_staff:
                return Response({
                    'status': False,
                    'status_code': 1,
                    'message': 'Invalid password'
                })
            user_profile = Profile.objects.filter(user = user).first()
            user_profile_serialize = ProfileSerializer(user_profile)
            if not user.check_password(password):
                return Response({
                    'status': False,
                    'status_code': 1,
                    'message': 'Invalid password'
                })
            #user, token = AuthToken.objects.create(user)
            user.last_login = timezone.now()
            user.save()
            #save date
            refresh = RefreshToken.for_user(user)
            refresh['username'] = user.username
            refresh['email'] = user.email
            refresh['date_logged'] = str(datetime.now())

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
        
class crateSignupCode(APIView):
    def post(self, request:HttpRequest):
        id = uuid.uuid4()
        email = request.data['email']
        username = request.data['username']
        code = random.randint(100000, 999999)
        expiration = datetime.now()+timedelta(minutes=5)
        try:
            User.objects.get(email = email)
            return Response({"status": False, "status_code": 200, "message": "email already exists"})
        except User.DoesNotExist:
            pass

        a = UserRegisterCode.objects.filter(expiration__gt = Now())
        try:
            a.get(email = email)
            return Response({"status": False, "status_code": 200, "message": "already requested please wait 5 minutes"})
        except:
            pass
        data = {"id": id, "email": email, "username": username, "code": code, "expiration": str(expiration)}
        serialiser = UserRegisterCodeSerializer(data = data)
        if serialiser.is_valid():
            if sendEmailFromUser(code=code, useremail=email):
                serialiser.save()
                return Response({"status": True, "status_code": 200, "message": "authentication created", 'data': {'regId': id, 'email': email, 'username': username}})
            


        return Response({"status": False, "status_code": 200, "message": "invalid cridentials"})


class signup(APIView):
    def createAccount(self, name, username, email, password):
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
        refresh = RefreshToken.for_user(user_model)
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
                    'refresh_token': str(refresh),
                    'tokenType': 'Bearer',
                    'accesstoken': str(refresh.access_token)
                    }})
        
    def checkCridential(self, code, regId, email):
        #a = UserRegisterCode.objects.filter(expiration__gt=Now())
        try:
            b = UserRegisterCode.objects.get(id = str(regId), expiration__gt=Now())
            print(b)
        except UserRegisterCode.DoesNotExist as e:
            print(f"Error: {e}")
            return False
        except ValidationError as e:
            print(f"Error: {e}")
            return False
        if b.email == email and b.code == code:
            print(f"New success registrations")
            return True



    def post(self, request:HttpRequest):
        code = request.data['code']
        regId = request.data['cridential']
        username = request.data['username']
        email = request.data['email']
        name = request.data['name'].split()
        password = request.data['password']
        password2 = request.data['password2']
        print(code, regId, username, email, name, password, password2)
        if password != password2:
            return Response({
                'status': False,
                'message': 'Password not matches'
            })
 
        if User.objects.filter(email=email).exists():
            return Response({
                'status':False,
                'message': 'Email already exists'})
        
        if User.objects.filter(username=username).exists():
            return Response({
                'status':False,
                'message': 'Username already exists'})
        
        
        if UserRegisterCode.objects.filter(id = regId, expiration__gt = Now()).exists():
            registerCodeTable = UserRegisterCode.objects.get(id = str(regId))
            
            if str(registerCodeTable.code).strip() != str(code).strip():
                print(registerCodeTable.code, code)
                return Response({"status": False, 
                                 "status_code": 200, 
                                 "message": "invalid code"
                                 })
            elif str(registerCodeTable.email).strip() != str(email).strip():
                return Response({"status": False, 
                                 "status_code": 200, 
                                 "message": "invalid registered email"
                                 })
            else:
                return self.createAccount(name = name, username=username, email=email, password=password)
        else:
            return Response({"status": False, 
                             "status_code": 200, 
                             "message": "Expired code"
                             })
   