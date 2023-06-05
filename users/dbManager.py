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
from django.utils import timezone
from datetime import datetime
from django.http import HttpRequest
import time
from time_.get_time import getStringTime, getStringTimeForSwitchAccount

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
