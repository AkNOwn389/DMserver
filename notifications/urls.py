from django.urls import path
from . import views

urlpatterns = [
    path("my/page=<int:page>", views.MyNotificationView.as_view(), name="mynotifications"),
    path("notificationBadge", views.NotificationBadgeView.as_view(), name="Notifbadge"),
    path("chatBadge", views.ChatBadge.as_view(), name="chatbadge"),
    path('seen/id=<int:id>', views.Seen.as_view(), name = 'Seen'),
    path('delete/id=<int:id>', views.Delete.as_view(), name = 'Delete'),
    path("notify", views.Notify.as_view(), name="notify"),
]