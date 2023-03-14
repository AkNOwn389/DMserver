from rest_framework.authentication import get_authorization_header, BaseAuthentication
from django.contrib.auth.models import User
from rest_framework import exceptions
from django.conf import settings
import jwt

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode("utf-8")
        auth_token = auth_data.split(" ")
        if len(auth_token) !=2:
            raise exceptions.AuthenticationFailed("invalid token")
        token = auth_data[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms=["HS256"])
            username = payload['username']
            user = User.objects.get(username = username)
            return (user, token)
        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed("token expired")
        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed("token invalid")
        except User.DoesNotExist as noUser:
            raise exceptions.AuthenticationFailed("User Not Exists")

        return super.authenticate(request)