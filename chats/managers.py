from django.db import models
from django.db.models import Count
from .models import PrivateMessage
from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser

class MessageManager(models.Manager):
    def getMainPageView(self, user:AbstractBaseUser) -> list[PrivateMessage]:
        messages = PrivateMessage.objects.filter(Q(sender = user) | Q(receiver = user)).order_by("-date_time")
        msg_lists = []
        msg = []
        for x in messages:
            y = x.sender if x.receiver == user else x.receiver
            if y not in msg:
                msg.append(y)
                msg_lists.append(x)
        return msg_lists