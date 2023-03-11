from django.urls import path
from . import views
urlpatterns = [
    path('following/page=<int:page>', views.get_following_list.as_view(), name="following"),
    path('followers/page=<int:page>', views.get_follower.as_view(), name='followers'),
    path('signup', views.signup.as_view(), name='signup'),
    path('login', views.login.as_view(), name='login'),
    path('logout', views.logout.as_view(), name='logout'),
]
