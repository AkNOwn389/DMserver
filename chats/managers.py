from django.db import models
from django.db.models import Count
from .models import PrivateMessage
from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def room_sender(room: str, event: dict) -> bool:
    try: 
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(room, event)
        return True
    except Exception as e:
        print(e)
        return False
    
def get_chat_page_channel_name(username: str) -> str:
    return f"room_{username}_on_chat_page"

def get_chat_user_room_name(username: str) -> str:
    return f"room_{username}_on_chat"