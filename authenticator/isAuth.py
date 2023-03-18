from django.conf import settings
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken
from django.contrib.auth.models import User
import jwt

def AuthUser(user):
    try:
        token = user.headers['Authorization'].split()[1]
    except:
        False
    try:
        decode_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHYM])
    except jwt.ExpiredSignatureError:
        return False
    except jwt.DecodeError:
        return False
    except jwt.InvalidTokenError:
        return False
    
    try:
        User.objects.get(username = decode_token['username'])
    except User.DoesNotExist:
        return False
    
    return True

