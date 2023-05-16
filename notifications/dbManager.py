from typing import Awaitable

from .models import MyNotification
from django.contrib.auth.models import AbstractBaseUser
from channels.db import database_sync_to_async
from .models import NotificationChannel
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from chats.models import PrivateMessage, RoomManager

def getSeenNotification(user: AbstractBaseUser) -> MyNotification:
    return MyNotification.objects.filter(userToNotify=user, seen=True)


def getUnseenNotification(user: AbstractBaseUser) -> MyNotification:
    return MyNotification.objects.filter(userToNotify=user, seen=False)


def getAllNotification(user: AbstractBaseUser) -> MyNotification:
    return MyNotification.objects.filter(userToNotify=user)


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
    async_to_sync(channel_layer.group_send)(room, event)
    return

def notifBadge(user:AbstractBaseUser):
    notif = MyNotification.objects.filter(userToNotify=user, seen=False)
    return len(notif) if len(notif) < 100 else 99


def chatBadge(user:AbstractBaseUser):
    notif = RoomManager().get_all_unread_message(user=user)
    return len(notif) if len(notif) < 100 else 99

def pushBadge(creator:AbstractBaseUser) -> None:
        len_notif = notifBadge(user=creator)
        len_chat = chatBadge(user=creator)
        room = getOrCreateNotificationChannel(user = creator)
        event = {
            'status': True,
            'status_code': 200,
            'type': 'new_notification_badge',
            'notification': len_notif,
            'chat': len_chat}
        pustNotifications(event=event, room=room)