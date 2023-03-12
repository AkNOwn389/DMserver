from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('post/', include('posts.urls')),
    path('profile/', include('profiles.urls')),
    path('feed/', include('feeds.urls')),
    path('chat/', include('chats.urls')),
    path('user/', include('users.urls')),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]