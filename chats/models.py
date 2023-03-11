from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile
from datetime import datetime
import uuid
_now = datetime.now()

# Create your models here.
class Room(models.Model):
    subscribers = models.ManyToManyField(Profile, blank=True) #(1)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class RoomMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    msg_sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField(max_length=1500)

    def __str__(self):

        return self.body
#user.add(profile)
#users_in_1zone = User.objects.filter(zones__id=<id1>)
#users_in_1zone = User.objects.filter(zones__in=[<id1>]
#users_in_zones = User.objects.filter(zones__in=[zone1, zone2, zone3])
#users_in_zones = User.objects.filter(zones__in=[<id1>, <id2>, <id3>])
#python manage.py migrate --run-syncdb

class ChatRoom(models.Model):
    chat_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    users = models.ManyToManyField(User, related_name="room_user")

    
class ChatMessage(models.Model):
    messageid = models.UUIDField(unique=False)
    msg_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_sender")
    msg_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_receiver") 
    body = models.TextField(max_length=1500)
    created_at = models.DateField(default=_now.strftime("%Y-%m-%d"))
    created_time = models.TimeField(default=(f"{_now.hour}:{_now.minute}:{_now.second}.{_now.microsecond}"))
    seen = models.BooleanField(default=False)

    def __str__(self):
        return str(self.msg_sender)+' to '+str(self.msg_receiver)

class OnlineUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username
