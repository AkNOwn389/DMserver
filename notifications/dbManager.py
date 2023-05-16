from typing import Awaitable

from .models import MyNotification
from django.contrib.auth.models import AbstractBaseUser
from channels.db import database_sync_to_async
from .models import NotificationChannel
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def getSeenNotification(user: AbstractBaseUser) -> MyNotification:
    return MyNotification.objects.filter(userToNotify=user, seen=True)


def getUnseenNotification(user: AbstractBaseUser) -> MyNotification:
    return MyNotification.objects.filter(userToNotify=user, seen=False)


def getAllNotification(user: AbstractBaseUser) -> MyNotification:
    return MyNotification.objects.filter(userToNotify=user)


@database_sync_to_async
def getOrCreateNotificationChannel(user: AbstractBaseUser) -> Awaitable[str]:
    if NotificationChannel.objects.filter(user=user).exists():
        room: NotificationChannel = NotificationChannel.objects.get(user=user)
        print(room.channel_room)
        return str(room.channel_room)
    else:
        room = NotificationChannel.objects.create(user=user).save()
        print(room.channel_room)
        return str(room.channel_room)


def pustNotifications(event:dict, room:str) -> None:
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(room,event)
    return

