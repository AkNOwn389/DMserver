from django.urls import path
from . import views

urlpatterns = [
    path('sendmessage', views.sendmessage.as_view(), name='sendmessage'),
    #path('mychatpage/page=<int:page>', views.MessagePageView.as_view(), name='mymessage'),
    path('getmessage/<str:pk>/page=<int:page>', views.GetMessageView.as_view(), name="mymessage"),
    #path('messagepage/page=<int:page>', views.MessagePageView.as_view(), name="messagePage"),
    path('notify', views.Notify.as_view(), name="notify"),
    path('notify/<str:user>', views.ChatListener.as_view(), name='chatlistener'),
    path('seen/<str:id>', views.Seen.as_view(), name='seen'),
    path('deleteMessage/id=<int:id>', views.DeleleMessage.as_view(), name="delete_message")
]