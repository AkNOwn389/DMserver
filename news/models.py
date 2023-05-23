from django.db import models
from django.utils import timezone
import uuid


class News(models.Model):
    DoesNotExist = None
    objects = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    avatar = models.URLField(blank=True)
    title = models.TextField(blank=True)
    news_id = models.TextField(blank=True)
    name = models.TextField(blank=True)
    author = models.TextField(blank=True)
    description = models.TextField(blank=True)
    url = models.URLField(blank=False, null=False)
    urlToImage = models.URLField(blank=True)
    publishedAt = models.DateTimeField(default=timezone.now())
    content = models.TextField(blank=True)
    noOfLike = models.IntegerField(default=0)
    NoOfComment = models.IntegerField(default=0)
    noOfShare = models.IntegerField(default=0)
    news_type = models.IntegerField(default=1)

    def __str__(self):
        return self.title
