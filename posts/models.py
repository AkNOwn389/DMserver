from django.contrib.auth.models import User
from django.db import models
import uuid, random, os

# Create your models here.
def post_rdm_name(a, b):
    c, d = os.path.splitext(b)
    while True:
        e = ''.join((str(random.randint(0, 9))) for x in range(40))
        f = f"post_images/{str(e)}{str(d)}"
        g = Images.objects.filter(image=f).first()
        if g is None:
            return str(f)
    
def post_videos_rdm_name(a, b):
    c, d = os.path.splitext(b)
    while True:
        e = ''.join((str(random.randint(0, 9))) for x in range(40))
        f = f"post_avatar/{str(c)}-{str(a)}-{str(e)}-{str(d)}"
        g = Post.objects.filter(images_url=f).first()
        if g is None:
            return f
class Images(models.Model):
    image = models.ImageField(max_length=500, upload_to=post_rdm_name, verbose_name="Image")
    class Meta:
        ordering = ['image']
    def __str__(self):
        return self.image

class Videos(models.Model):
    videos = models.ImageField(upload_to=post_videos_rdm_name)
    class Meta:
        ordering = ['videos']
    def __str__(self):
        return self.videos
    
class Post(models.Model):
    id = models.UUIDField(primary_key = True, default=uuid.uuid4)
    source = models.TextField(max_length=200, default="direct message")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    creator_full_name = models.TextField(max_length=200)
    images_url = models.ManyToManyField(Images, blank=True)
    videos_url = models.ManyToManyField(Videos, blank=True)
    title = models.TextField(blank=True)
    perma_link = models.TextField(blank=True)
    description = models.TextField(blank=True)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    NoOflike = models.IntegerField(default=0)
    NoOfcomment = models.IntegerField(default=0)
    media_type = models.IntegerField(default=1)
    def __str__(self):
        return str(self.creator)+" "+self.description

class Postcomment(models.Model):
    post_id = models.UUIDField(primary_key=True)
    avatar = models.ImageField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField(max_length=1500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_id

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.username)