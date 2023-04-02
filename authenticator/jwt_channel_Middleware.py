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
        user = User.objects.get(id = USER)
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
                token = x[1].decode().split()[1]
                
                
        if token is None:
            scope['user'] = AnonymousUser()
        else:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHYM])
            username = payload['user_id']
            scope['user'] = await get_user(username)
            
            

        return await super().__call__(scope, receive, send)