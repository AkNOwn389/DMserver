import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class NotificationChannel(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_notification_consumer")
    channel_room = models.TextField(default=uuid.uuid4())

    def __str__(self):
        return self.channel_room


class MyNotification(models.Model):
    objects = None
    userToNotify = models.ForeignKey(User, blank=False, related_name="user_to_notify", on_delete=models.CASCADE, default=None)
    subjectUser = models.ManyToManyField(User, blank=False, related_name='subjectUser')
    subjectPostsId = models.TextField(blank=True, default=None)
    title = models.TextField(max_length=500, blank=False)
    description = models.TextField(max_length=1500)
    notifType = models.IntegerField(blank=False)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["seen", "-date", ]

    def __str__(self):
        return self.title
