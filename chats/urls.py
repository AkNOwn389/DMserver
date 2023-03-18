from django.urls import path
from . import views

urlpatterns = [
    path('sendmessage', views.sendmessage.as_view(), name='sendmessage'),
    path('mychatpage/page=<int:page>', views.MessagePageView.as_view(), name='mymessage?'),
    path('getmessage/<str:pk>/page=<int:page>', views.GetMessageView.as_view(), name="mymessage"),
    path('messagepage/page=<int:page>', views.MessagePageView.as_view(), name="messagePage"),
]