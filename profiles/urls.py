from django.urls import path
from . import views

urlpatterns = [
    path('profilePictureUpdate', views.ProfilePictureUpdate.as_view(), name='profileupdate'),
    path('profileCoverUpdate', views.ProfileCoverUpdate.as_view(), name="coverupdate"),
    path('updatedetails', views.UpdateDetails.as_view(), name='update_details'),
    path('search/<str:user>/page=<int:page>', views.search.as_view(), name='search'),
    path('mainsearch/type=<str:type>/search=<str:user>/page=<int:page>', views.MainSearch.as_view(), name='mainsearch'),
    path("getavatar/<str:user>", views.avatarView.as_view(), name = "getavatar"),
    path('user/<str:user>', views.profile.as_view(), name='profile'),
    path("save-recent/<str:user>", views.SaveRecentSearch.as_view(), name='save-recent'),
    path("search/recent", views.GetRecentSearch.as_view(), name = "recent"),
    path('me', views.Me.as_view(), name='me'),
]
