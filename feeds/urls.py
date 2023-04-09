from django.urls import path
from . import views
urlpatterns = [
    path('newsfeed/page=<int:page>', views.newsfeed.as_view(), name='newsfeed'),
    path('videofeed/page=<int:page>', views.VideosFeed.as_view(), name='videofeed'),
    path('mypost/page=<int:page>', views.MyPostView.as_view(), name='mypostshistory')
]
