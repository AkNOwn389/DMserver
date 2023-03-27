from django.urls import path
from . import views

urlpatterns = [
    path("my/page=<int:page>", views.MyNotificationView.as_view(), name="mynotifications"),
    path("notify", views.Notify.as_view(), name="notify")
]