from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken
from Authentication.models import UserRegisterCode, UserRecoveryCode
from Authentication.serializers import UserRegisterCodeSerializer, UserRecoveryCodeSerializer
from users.models import FollowerCount
from rest_framework.views import APIView
from django.http import JsonResponse
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
from .models import OnlineUser
from smtplib import SMTPRecipientsRefused
import random, uuid
from .serializers import OnlineUserSerializer
from django.utils import timezone
from datetime import datetime
from django.http import HttpRequest
import time
from .models import OnlineUser, FollowerCount
from time_.get_time import getStringTime, getStringTimeForSwitchAccount
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



@database_sync_to_async
def getOnlineUser(user:AbstractBaseUser) -> dict[OnlineUserSerializer]:
    friends = FollowerCount.objects.filter(follower = user)
    online_friends = OnlineUser.objects.none()
    
    if friends:
        for i in friends:
            online_friends |= OnlineUser.objects.filter(user = i.user)
    if len(online_friends) != 0:
        data = OnlineUserSerializer(online_friends, many = True).data
        return data
    else:
        return None

@database_sync_to_async
def ImOnline(user: AbstractBaseUser) -> bool:
    channel_layer = get_channel_layer()
    try:
        friends = FollowerCount.objects.filter(user = user)
        profile = Profile.objects.get(user = user)
        serialize_profile = ProfileSerializer(profile).data
        text = {"avatar":serialize_profile['profileimg'],
                "name": serialize_profile['name'],
                "id": user.pk,
                "username": user.username,
                "type": "new_online_user"
                }
        if friends is not None:
            for i in friends:
                room = str(f"room_{i.follower.username}")
                async_to_sync(channel_layer.group_send)(room, text)
                
        return True
    
    except:
        return False
@database_sync_to_async
def ImOffline(user: AbstractBaseUser) -> bool:
    channel_layer = get_channel_layer()
    try:
        friends = FollowerCount.objects.filter(user = user)
        profile = Profile.objects.get(user = user)
        serialize_profile = ProfileSerializer(profile).data
        text = {"avatar":serialize_profile['profileimg'],
                "name": serialize_profile['name'],
                "id": user.pk,
                "username": user.username,
                "type": "new_offline_user"
                }
        if friends is not None:
            for i in friends:
                room = str(f"room_{i.follower.username}")
                async_to_sync(channel_layer.group_send)(room, text)
                
        return True
    
    except:
        return False
            


def sendRecoveryCodeEmailFromUser(code, useremail):
    email = EmailMessage('Recovery code from DM',
                            '(DM) Your one time otp code is  {} \nIf you not requesting otp do not share this on others.'.format(str(code)),
                            settings.EMAIL_HOST_USER,
                            [useremail],
                            )
    email.fail_silently = False
    try:
        email.send()
        return True
    except SMTPRecipientsRefused:
        return False
    
def sendEmailFromUser(code, useremail):
    email = EmailMessage('Thanks for signing directmessage app here\'s your code',
                            '(DM) Your one time otp code is  {} \nIf you not requesting otp do not share this on others.'.format(str(code)),
                            settings.EMAIL_HOST_USER,
                            [useremail],
                            )
    email.fail_silently = False
    try:
        email.send()
        return True
    except SMTPRecipientsRefused:
        return False
    
def get_client_ip(request:HttpRequest):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
