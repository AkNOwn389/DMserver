from django.db import models
from django.contrib.auth.models import User
import sys



# Create your models here.
class FollowerCount(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

    def __str__(self):
        return "user: "+str(self.user)+" follower: "+str(self.follower)
    
class OnlineUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username