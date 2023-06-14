from django.urls import path
from . import views
urlpatterns = [
    path('feeds/page=<int:page>', views.Stories.as_view()),
]