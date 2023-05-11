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
import cloudinary, json, datetime
from typing import Optional, Iterable
from cloudinary import CloudinaryImage, CloudinaryVideo, CloudinaryResource
from cloudinary.utils import cloudinary_url


def getAssetInfo(public_id):
    # Get and use details of the image
    # ==============================
    # Get image details and save it in the variable 'image_info'.
    image_info = cloudinary.api.resource(public_id)
    print("****3. Get and use details of the image****\nUpload response:\n", json.dumps(image_info, indent=2), "\n")
    return image_info


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
        if Post.objects.filter(id=a).first():
            go = False
        if Image.objects.filter(id=a).first():
            go = False
        if Videos.objects.filter(id=a).first():
            go = False
        if go == True:
            return a


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=get_unique_id)
    public_id = models.TextField(max_length=300, blank=False, default="null")
    image = CloudinaryField("image", folder="media/post_images/")
    NoOflike = models.IntegerField(default=0)
    NoOfcomment = models.IntegerField(default=0)
    url = models.URLField(blank=True)
    url_w1000 = models.URLField(blank=True)
    url_w250 = models.URLField(blank=True)
    secure_url = models.URLField(blank=True)
    width = models.TextField(blank=True)
    height = models.TextField(blank=True)
    thumbnail = models.TextField(blank=True)
    asset_id = models.TextField(blank=True)
    version = models.TextField(blank=True)
    version_id = models.TextField(blank=True)
    signature = models.TextField(blank=True)
    Format = models.TextField(blank=True)
    resource_type = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    Bytes = models.TextField(blank=True)
    Type = models.TextField(blank=True)
    etag = models.TextField(blank=True)

    class Meta:
        ordering = ['image', 'NoOflike', 'NoOfcomment', 'thumbnail']

    def __str__(self):
        return str(self.id)

    def update(self, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            upload_result = cloudinary.uploader.upload(self.image,
                                                       options={"quality": "auto:low", 'width': 500, 'crop': "scale"})
            self.url = upload_result['url']
            self.secure_url = upload_result['secure_url']
            self.public_id = upload_result['public_id']
            self.width = upload_result['width']
            self.height = upload_result['height']
            self.asset_id = upload_result['asset_id']
            self.version = upload_result['version']
            self.version_id = upload_result['version_id']
            self.signature = upload_result['signature']
            self.Format = upload_result['format']
            self.resource_type = upload_result['resource_type']
            self.created_at = upload_result['created_at']
            self.Bytes = upload_result['bytes']
            self.Type = upload_result['type']
            self.etag = upload_result['etag']
            url, options = cloudinary_url(
                upload_result['public_id'],
                transformation=[{'width': 1000, 'crop': "scale"}, {'quality': "auto"}, {'fetch_format': "auto"}]
            )
            self.url_w1000 = url
            url, options = cloudinary_url(
                upload_result['public_id'],
                transformation=[{'width': 500, 'crop': "scale"}, {'quality': "auto"}, {'fetch_format': "auto"}]
            )
            self.thumbnail = url
            url, options = cloudinary_url(
                upload_result['public_id'],
                transformation=[{'width': 250, 'crop': "scale"}, {'quality': "auto"}, {'fetch_format': "auto"}]
            )
            self.url_w250 = url
        except Exception as e:
            cloudinary.uploader.destroy(self.public_id)
            print(e)
            return
        super(Image, self).save(*args, **kwargs)


class Videos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    public_id = models.TextField(max_length=300, blank=False, default="null")
    videos = CloudinaryField("video", resource_type="video", folder="post_videos/")
    # video url
    original = models.URLField(blank=True)
    playback_url = models.URLField(blank=True)
    url_w1000 = models.URLField(blank=True)
    url_w500 = models.URLField(blank=True)
    url_w250 = models.URLField(blank=True)
    # data
    secure_url = models.URLField(blank=True)
    audio_bit_rate = models.TextField(blank=True)
    audio_codec = models.TextField(blank=True)
    frequency = models.TextField(blank=True)
    channels = models.TextField(blank=True)
    channel_layout = models.TextField(blank=True)
    width = models.TextField(blank=True)
    height = models.TextField(blank=True)
    thumbnail = models.URLField(blank=True)
    asset_id = models.TextField(blank=True)
    version = models.TextField(blank=True)
    version_id = models.TextField(blank=True)
    signature = models.TextField(blank=True)
    Format = models.TextField(blank=True)
    resource_type = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    Bytes = models.TextField(blank=True)
    Type = models.TextField(blank=True)
    etag = models.TextField(blank=True)
    is_audio = models.BooleanField(default=False)
    framerate = models.IntegerField(blank=True)
    bit_rate = models.TextField(blank=True)
    duration = models.IntegerField(blank=True)
    rotation = models.IntegerField(default=0)
    original_filename = models.TextField(blank=True)
    nb_frames = models.IntegerField(blank=True)
    api_key = models.TextField(blank=True)
    # video
    pix_format = models.TextField(blank=True)
    video_codec = models.TextField(blank=True)
    level = models.TextField(blank=True)
    profile = models.TextField(blank=True)
    video_bitrate = models.TextField(blank=True)
    time_base = models.TextField(blank=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        # upload video
        upload_result = cloudinary.uploader.upload(self.videos, resource_type="auto")
        # assigning value
        self.original = upload_result['url']
        self.playback_url = upload_result['playback_url']
        self.secure_url = upload_result['secure_url']
        self.public_id = upload_result['public_id']
        self.width = upload_result['width']
        self.height = upload_result['height']
        self.asset_id = upload_result['asset_id']
        self.version = upload_result['version']
        self.version_id = upload_result['version_id']
        self.signature = upload_result['signature']
        self.Format = upload_result['format']
        self.resource_type = upload_result['resource_type']
        self.created_at = upload_result['created_at']
        self.Bytes = upload_result['bytes']
        self.Type = upload_result['type']
        self.etag = upload_result['etag']
        # datails
        # audio
        self.audio_bit_rate = upload_result['audio']['bit_rate']
        self.audio_codec = upload_result['audio']['codec']
        self.frequency = upload_result['audio']['frequency']
        self.channels = upload_result['audio']['channels']
        self.channel_layout = upload_result['audio']['channel_layout']
        # video
        self.pix_format = upload_result['video']['pix_format']
        self.video_codec = upload_result['video']['codec']
        self.level = upload_result['video']['level']
        self.profile = upload_result['video']['profile']
        self.video_bitrate = upload_result['video']['bit_rate']
        self.time_base = upload_result['video']['time_base']
        # all
        self.is_audio = upload_result['is_audio']
        self.framerate = upload_result['frame_rate']
        self.bit_rate = upload_result['bit_rate']
        self.duration = upload_result['duration']
        self.rotation = upload_result['rotation']
        self.original_filename = upload_result['original_filename']
        self.nb_frames = upload_result['nb_frames']
        self.api_key = upload_result['api_key']
        try:
            url, options = cloudinary_url(
                upload_result['public_id'],
                resource_type='video',
                transformation=[{'width': 1000, 'crop': "scale"}, {'quality': "auto"}, {'fetch_format': "auto"}]
            )
            self.url_w1000 = url
        except Exception as e:
            print(f"Exception: {e}")
            pass
        try:
            url, options = cloudinary_url(
                upload_result['public_id'],
                resource_type='video',
                transformation=[{'width': 500, 'crop': "scale"}, {'quality': "auto"}, {'fetch_format': "auto"}]
            )
            self.url_w500 = url
        except Exception as e:
            print(f"Exception: {e}")
            pass
        try:
            url, options = cloudinary_url(
                upload_result['public_id'],
                resource_type='video',
                transformation=[{'width': 250, 'crop': "scale"}, {'quality': "auto"}, {'fetch_format': "auto"}]
            )
            self.url_w250 = url
        except Exception as e:
            print(f"Exception: {e}")
            pass
        try:
            video = CloudinaryVideo(self.public_id)
            thumbnail_url = video.build_url(transformation=[{'quality': "auto"}, {'width': 1000, 'crop': 'scale'}],
                                            format='jpg')
            self.thumbnail = thumbnail_url
        except Exception as e:
            print(f"Exception: {e}")
            pass
        try:
            super(Videos, self).save(*args, **kwargs)
        except Exception as e:
            print(e)
            return


class Post(models.Model):
    DoesNotExist = None
    objects = None

    class privacy_choice(models.TextChoices):
        Public = 'P', _('Public')
        Friends = 'F', _('Friends')
        OnlyMe = 'O', _('Only-Me')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
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
    NoOfComment = models.IntegerField(default=0)
    media_type = models.IntegerField(default=1)
    privacy = models.CharField(choices=privacy_choice.choices, default=privacy_choice.Friends, max_length=1)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.creator) + " " + str(self.description)

    def update(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)


class SharePost(models.Model):
    class privacy_choice(models.TextChoices):
        Public = 'P', _('Public')
        Friends = 'F', _('Friends')
        OnlyMe = 'O', _('Only-Me')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    postToShare = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_to_share')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='share_post_creator')
    creator_full_name = models.TextField(max_length=200)
    description = models.TextField(blank=True)
    title = models.TextField(blank=True)
    privacy = models.CharField(choices=privacy_choice.choices, default=privacy_choice.Friends, max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    NoOflike = models.IntegerField(default=0)
    NoOfcomment = models.IntegerField(default=0)
    media_type = models.IntegerField(default=1)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.creator) + " " + str(self.description)

    def update(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)


class LikePost(models.Model):
    objects = None

    class ReactionType(models.TextChoices):
        HAPPY = 'H', 'Happy'
        LOVE = 'L', 'Love'
        LIKE = 'T', 'Like'
        SAD = 'S', 'Sad'
        WOW = 'W', 'Wow'
        ANGRY = 'A', 'Angry'

    post_id = models.CharField(max_length=500)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    reactionType = models.CharField(
        max_length=1,
        choices=ReactionType.choices,
        default=ReactionType.LIKE,
    )

    def __str__(self):
        return str(self.username)
