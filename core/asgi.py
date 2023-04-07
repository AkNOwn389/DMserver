"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from authenticator.jwt_channel_Middleware import TokenAuthMiddleware#, HttpTokenMiddleWare
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

from routers import channel_routing
application = ProtocolTypeRouter({'http': get_asgi_application(),"websocket": TokenAuthMiddleware(AuthMiddlewareStack(URLRouter(channel_routing.websocket_urlpatterns)))})

#application = ProtocolTypeRouter({"websocket":TokenAuthMiddleware( AuthMiddlewareStack(URLRouter(channel_routing.websocket_urlpatterns))),})