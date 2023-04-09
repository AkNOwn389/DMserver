from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from moviepy.editor import VideoFileClip
from cloudinary_storage.storage import RawMediaCloudinaryStorage, VideoMediaCloudinaryStorage, MediaCloudinaryStorage
import uuid, random, os
from PIL import Image as ImagePIL
from io import BytesIO, StringIO
from django.core.files import File
from cloudinary.forms import CloudinaryFileField
from cloudinary.models import CloudinaryField


# Create your models here.
def post_rdm_name(a, b):
    c, d = os.path.splitext(b)
    while True:
        e = ''.join((str(random.randint(0, 9))) for x in range(10))
        f = f"post_images/{str(e)}{str(d)}".encode('utf-8').decode()
        f = f.replace(" ", "-")
        g = Image.objects.filter(image=f).first()
        if g is None:
            return str(f)
    
def post_videos_rdm_name(a, b):
    c, d = os.path.splitext(b)
    while True:
        e = ''.join((str(random.randint(0, 9))) for x in range(10))
        f = f"post_videos/{str(e)}-{str(d)}".encode('utf-8').decode()
        f = f.replace(" ", "-")
        g = Videos.objects.filter(videos=f).first()
        if g is None:
            return f
        
def get_unique_id():
    while True:
        a = uuid.uuid4()
        go = True
        if Post.objects.filter(id = a).first():
            go = False
        if Image.objects.filter(id = a).first():
            go = False
        if Videos.objects.filter(id = a).first():
            go = False
        if go == True:
            return a

class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=get_unique_id)
    image = models.ImageField(max_length=500, upload_to=post_rdm_name, verbose_name="Image", storage=MediaCloudinaryStorage())
    width = models.TextField(blank=True)
    heigth = models.TextField(blank=True)
    NoOflike = models.IntegerField(default=0)
    NoOfcomment = models.IntegerField(default=0)
    thumbnail = models.ImageField(upload_to='posts_images/thumbnails/', blank=True,  verbose_name='thumbnail', storage=MediaCloudinaryStorage())
    class Meta:
        ordering = ['image', 'NoOflike', 'NoOfcomment', 'thumbnail']
    def __str__(self):
        return str(self.id)

class Videos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    thumbnail = models.ImageField(blank=True, storage=MediaCloudinaryStorage())
    videos = models.FileField(upload_to=post_videos_rdm_name, storage=VideoMediaCloudinaryStorage())
    """
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        clip = VideoFileClip(self.videos.path)
        thumbnail = clip.subclip(0, 10).save_frame(self.thumbnail.path)
        """

    class Meta:
        ordering = ['videos', 'thumbnail']
        
    def __str__(self):
        return str(self.id)
    
class Post(models.Model):
    class privacy_choice(models.TextChoices):
        Public = 'P', _('Public')
        Friends = 'F', _('Friends')
        OnlyMe = 'O', _('Only-Me')

    id = models.UUIDField(primary_key = True, default=uuid.uuid4)
    source = models.TextField(max_length=200, default="direct message")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    creator_full_name = models.TextField(max_length=200)
    images_url = models.ManyToManyField(Image, blank=True, related_name="images")
    videos_url = models.ManyToManyField(Videos, blank=True, related_name="video")
    title = models.TextField(blank=True)
    perma_link = models.TextField(blank=True)
    description = models.TextField(blank=True)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    NoOflike = models.IntegerField(default=0)
    NoOfcomment = models.IntegerField(default=0)
    media_type = models.IntegerField(default=1)
    privacy = models.CharField(choices=privacy_choice.choices, default=privacy_choice.Friends, max_length=1)
    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        return str(self.creator)+" "+str(self.description)

class Comment(models.Model):
    post_id = models.UUIDField(primary_key=False)
    avatar = models.ImageField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, storage=MediaCloudinaryStorage())
    type = models.IntegerField(blank=False, default=1)
    comments = models.TextField(max_length=1500)
    created = models.DateTimeField(auto_now_add=True)
    NoOflike = models.IntegerField(default=0)

    def __str__(self):
        return self.post_id

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.username)

class LikeComment(models.Model):
    commentId = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)