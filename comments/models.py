from django.db import models
from django.contrib.auth.models import User
from posts.models import Image, Videos

# Create your models here.

class LikeComment(models.Model):
    class ReactionType(models.TextChoices):
        HAPPY = 'H', 'Happy'
        LOVE = 'L', 'Love'
        LIKE = 'T', 'Like'
        SAD = 'S', 'Sad'
        WOW = 'W', 'Wow'
        ANGRY = 'A', 'Angry'
    commentId = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reactionType = models.CharField(
        max_length=1,
        choices=ReactionType.choices,
        default=ReactionType.LIKE,
    )
    
class Comment(models.Model):
    post_id = models.UUIDField(primary_key=False)
    avatar = models.ImageField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ManyToManyField(Image, blank=True)
    video = models.ManyToManyField(Videos, blank=True)
    comment_type = models.IntegerField(blank=False, default=1)
    comments = models.TextField(max_length=1500)
    created = models.DateTimeField(auto_now_add=True)
    NoOflike = models.IntegerField(default=0)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.post_id