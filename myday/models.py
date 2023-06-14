from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
from posts.models import Image, Videos
import uuid
from datetime import timedelta, datetime
from django.utils import timezone

# Create your models here.

def get_expiration_time():
    time = timezone.now() + timedelta(days=1)
    return time

class UserStories(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, null=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    video = models.ForeignKey(Videos, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(default=get_expiration_time)
    no_of_comment = models.IntegerField(default=0)
    no_of_like = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return str(self.creator.username)