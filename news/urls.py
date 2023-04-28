from django.urls import path
from .views import GetNew



urlpatterns = [
    path('news/page=<int:page>', GetNew.as_view())
]