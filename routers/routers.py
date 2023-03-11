from django.urls import path, include

urlpatterns = [
    path('post/', include('posts.urls')),
    path('profile/', include('profiles.urls')),
    path('feed/', include('feeds.urls')),
    path('chat/', include('chats.urls')),
    path('user/', include('users.urls'))
]