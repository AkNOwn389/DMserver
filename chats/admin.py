from django.contrib import admin
from .models import singleOneToOneRoom, message
# Register your models here.
lists=[singleOneToOneRoom,
       message]
admin.site.register(lists)
