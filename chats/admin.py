from django.contrib import admin
from .models import ChatMessage, ChatRoom
# Register your models here.
lists=[ChatMessage,
       ChatRoom]
admin.site.register(lists)
