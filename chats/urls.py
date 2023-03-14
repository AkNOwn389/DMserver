from django.urls import path
from . import views

urlpatterns = [
    path('mychatpage/page=<int:page>', views.MessagePageView.as_view(), name='mymessage?'),
    #path('sendmessage', views.sendmessage.as_view(), name='sendmessage'),
    #path('getmessage', views.get_message.as_view(), name="mymessage"),
]