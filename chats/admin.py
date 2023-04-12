from django.contrib import admin
from .models import PrivateRoom, message
# Register your models here.
lists=[PrivateRoom,
       message]
admin.site.register(lists)
