from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, F
import uuid


class PrivateRoom(models.Model):
    temp_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_connector')
    connected_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatMate')

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
        return str(self.sender)+" "+str(self.receiver)
    
