from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.db.models import Q, F
from django.contrib.auth.models import AbstractBaseUser
import uuid, random
from django.conf import settings
from typing import Optional, Any
from django.utils.translation import gettext_lazy as _


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    e = ''.join((str(random.randint(0, 9))) for x in range(10))
    return f"user_{instance.uploaded_by.username}/{filename}-{str(e)}"

class UploadedFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Uploaded_by"),related_name='+', db_index=True)
    file = models.FileField(verbose_name=_("File"), blank=False, null=False, upload_to=user_directory_path)
    file_type = models.IntegerField(default=1)
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Upload date"))
    def __str__(self):
        return str(self.file.name)

class PrivateRoom(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_connector', null=False)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatMate', null=False)
    class Meta:
        unique_together = ["user1", "user2"]
    def __str__(self):
        return str(self.temp_id)
    

class RoomManager(models.Manager):
    def getOrCreateOneToOneRoom(self, user1, user2):
        qs = PrivateRoom.objects.filter(Q(user1 = user1, user2 = user2) | Q(user1 = user2, user2 = user1)).first()
        if qs is None:
            qs = PrivateRoom.objects.create(user1 = user1, user2 = user2)
            qs.save()
            return f"room_{qs.id}"
        elif qs is not None:
            return f"room_{qs.id}"
    def getMessagePagination(self, page:int, user1:AbstractBaseUser, user2:AbstractBaseUser):
        limit:int = settings.PAGE_LIMIT
        page:int = page*limit
        msg = PrivateMessage.objects.filter(Q(sender = user1, receiver = user2) | Q(sender = user2, receiver = user1)).order_by("-date_time")
        return msg[page-limit:page]
    
    def getMessageByTime(self, user1, user2):
        qs = PrivateMessage.objects.filter(Q(sender = user1, receiver = user2) | Q(sender = user2, receiver = user1)).order_by("-date_time")
        return qs

    def get_unread_count_for_dialog_with_user(self, sender, recipient):
        return PrivateMessage.objects.filter(reciever=sender, receiver=recipient, seen=False).count()
    
    def get_last_message_for_dialog(self, sender, recipient):
        return PrivateMessage.objects.filter(
            Q(sender=sender, receiver=recipient) | Q(sender=recipient, receiver=sender)) \
            .select_related('sender', 'recipient').first()
    
    def get_all_unread_message(self, user):
        return PrivateMessage.objects.filter(receiver = user, seen = False)
    

class PrivateMessage(models.Model):
    message_body = models.TextField()
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="msg_sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="msg_receiver")
    file = models.FileField(upload_to=user_directory_path, blank=True)
    image = models.ImageField(upload_to=user_directory_path, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    message_type = models.IntegerField(default=1)
    is_delete = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sender)
    
    class Meta:
        ordering = ('date_time',)
    



    
    
