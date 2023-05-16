from django.urls import path
from .views import GetNews



urlpatterns = [
    path('news/page=<int:page>', GetNews.as_view())
]