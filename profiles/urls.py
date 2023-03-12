from django.urls import path
from . import views

urlpatterns = [
    path('profilePictureUpdate', views.ProfilePictureUpdate.as_view(), name='profileupdate'),
    path('profileCoverUpdate', views.ProfileCoverUpdate.as_view(), name="coverupdate"),
    path('updatedetails', views.UpdateDetails.as_view(), name='update_details'),
    path('search/<str:user>/page=<int:page>', views.search.as_view(), name='search'),
    path("getavatar/<str:user>", views.avatarView.as_view(), name = "getavatar"),
    path('profile/<str:user>', views.profile.as_view(), name='profile'),
    path('follow/<str:user>', views.Follow.as_view(), name='follow'),
    path('me', views.Me.as_view(), name='me'),
]
