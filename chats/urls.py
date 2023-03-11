from django.urls import path
from . import views

urlpatterns = [
    path('sendmessage', views.sendmessage.as_view(), name='sendmessage'),
    path('getmessage', views.get_message.as_view(), name="mymessage"),
]