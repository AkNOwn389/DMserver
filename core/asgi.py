"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from authenticator.jwt_channel_Middleware import TokenAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

from routers import websocket_router
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    "websocket": TokenAuthMiddleware(AuthMiddlewareStack(
        URLRouter(
            websocket_router.websocket_urlpatterns
        )
    )),
})
