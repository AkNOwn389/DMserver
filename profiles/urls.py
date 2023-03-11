from django.urls import path
from . import views

urlpatterns = [
    path('profilepictureupdate', views.ProfilePictureUpdate.as_view(), name='profileupdate'),
    path('profilecoverupdate', views.ProfileCoverUpdate.as_view(), name="coverupdate"),
    path('search/<str:user>/page=<int:page>', views.search.as_view(), name='search'),
    path("getavatar/<str:user>", views.avatarView.as_view(), name = "getavatar"),
    path('profile/<str:user>', views.profile.as_view(), name='profile'),
    path('follow/<str:user>', views.Follow.as_view(), name='follow'),
    path('me', views.Me.as_view(), name='me'),
]
