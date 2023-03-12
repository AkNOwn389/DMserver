from django.contrib.auth.models import AnonymousUser
from knox.auth import AuthToken
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

@database_sync_to_async
def get_user(token_key):
    try:
        token = AuthToken.objects.get(token_key=token_key)
        return token.user
    except AuthToken.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        token_key = None
        headers = scope['headers']
        for x in headers:
            if (x[0].decode()) == "authorization":
                token_key = x[1].decode().split()[1][:8]
        if token_key is None:
            scope['user'] = AnonymousUser()
        else:
            scope['user'] = await get_user(token_key)
        return await super().__call__(scope, receive, send)