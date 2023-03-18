from django.urls import path
from . import views
urlpatterns = [
    path('newsfeed/page=<int:page>', views.newsfeed.as_view(), name='newsfeed'),
    path('mypost/page=<int:page>', views.MyPostView.as_view(), name='mypostshistory')
]
