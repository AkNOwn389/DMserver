from django.urls import path
from . import views
urlpatterns = [
    path('following/page=<int:page>', views.get_following_list.as_view(), name="following"),
    path('followers/page=<int:page>', views.get_follower.as_view(), name='followers'),
    path('usersuggested/page=<int:page>', views.user_suggested.as_view(), name='usersuggested'),
    path('cancelRequest/user=<str:user>', views.CancelRequest.as_view(), name = 'cancelRequest'),
    path('friends/page=<int:page>', views.get_friend.as_view(), name='friends'),
    path('signup/getCode', views.crateSignupCode.as_view(), name = 'getSignupCode'),
    path('follow/<str:user>', views.Follow.as_view(), name='follow'),
    path('denied/<str:user>', views.DeniedFollow.as_view(), name='deniedRequest'),
    path('signup', views.signup.as_view(), name='signup'),
    path('login', views.login.as_view(), name='login'),
    path('logout', views.logout.as_view(), name='logout'),
    path('islogged', views.WhoAmI.as_view(), name="islogged"),
]
