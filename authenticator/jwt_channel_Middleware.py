from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from rest_framework import exceptions
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings
import jwt

@database_sync_to_async
def get_user(USER):
    try:
        user = User.objects.get(username = USER)
        return user
    except User.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        token = None
        headers = scope['headers']
        for x in headers:
            if (x[0].decode()) == "authorization":
                auth_token = x[1].decode().split()
                if len(auth_token) !=2:
                    raise exceptions.AuthenticationFailed("invalid token")
                token = auth_token[1]
                
        if token is None:
            scope['user'] = AnonymousUser()
        else:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithns=settings.ALGO)
                username = payload['username']
                scope['user'] = await get_user(username)

            except jwt.ExpiredSignatureError as ex:
                raise exceptions.AuthenticationFailed("token expired")
            except jwt.DecodeError as ex:
                raise exceptions.AuthenticationFailed("token invalid")
            except User.DoesNotExist as noUser:
                raise exceptions.AuthenticationFailed("User Not Exists")
            
            

        return await super().__call__(scope, receive, send)