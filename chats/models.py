from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, F


class singleOneToOneRoom(models.Model):
    first_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="first_user", null=False)
    second_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="second_user", null=False)


    class Meta:
        unique_together = ["first_user", "second_user"]
        


class message(models.Model):
    message_body = models.TextField()
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="msg_sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="msg_receiver")
    date_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.room
    
