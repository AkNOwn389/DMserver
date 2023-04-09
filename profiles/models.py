from django.db import models
from django.contrib.auth.models import User
import random, os
from cloudinary_storage.storage import MediaCloudinaryStorage, VideoMediaCloudinaryStorage, RawMediaCloudinaryStorage, StaticHashedCloudinaryStorage, StaticCloudinaryStorage
# Create your models here.
def image_path(instance, filename):
    basefilename, file_extention = os.path.splitext(filename)
    while True:
        randomstr = ''.join((str(random.randint(0, 9))) for x in range(40))
        c = f"profile_image/{str(instance)}-{randomstr}{file_extention}"
        a = Profile.objects.filter(bgimg=c).first()
        b = Profile.objects.filter(profileimg=c).first()
        if a is None and b is None:
            return c
        
class Hobby(models.Model):
    hobby_name = models.TextField(max_length=200)

class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'None')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    bgimg = models.ImageField(upload_to=image_path, default='default-profile-picture_lxgxrl.jpg', storage=MediaCloudinaryStorage())
    profileimg = models.ImageField(upload_to=image_path, default='default-profile-picture_lxgxrl.jpg', storage=MediaCloudinaryStorage())
    interested = models.CharField(max_length=1, choices=GENDER_CHOICES, default="N")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="N")
    location = models.TextField(max_length=100, blank=True)
    school = models.TextField(max_length=1500, blank=True)
    works = models.TextField(max_length=500, blank=True)
    hobby = models.ManyToManyField(Hobby, max_length=200, blank=True)
    

    def __str__(self):
        return self.user.username
    
class RecentSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="search")
    searcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="searcher")
    date_search = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["date_search"]