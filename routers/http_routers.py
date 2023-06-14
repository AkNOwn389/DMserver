from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from Authentication.views import CustomTokenRefreshView

urlpatterns = [
    path('myday/', include('myday.urls')),
    path('post/', include('posts.urls')),
    path('comments/', include('comments.urls')),
    path('profile/', include('profiles.urls')),
    path('feed/', include('feeds.urls')),
    path('chat/', include('chats.urls')),
    path('user/', include('users.urls')),
    path('news/', include('news.urls')),
    path('notification/', include('notifications.urls')),
   # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]