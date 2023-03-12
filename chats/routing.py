from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
	path(
		r'test',
		consumers.ChatConsumer.as_asgi()
	),
    re_path(r'', consumers.Test.as_asgi())
]
