from django.urls import path
from . import views
urlpatterns = [
    path('newsfeed/page=<int:page>', views.newsfeed.as_view(), name='newsfeed'),
]
