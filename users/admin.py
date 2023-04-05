from django.contrib import admin
from .models import FollowerCount, OnlineUser
# Register your models here.
list = [FollowerCount,
        OnlineUser]
admin.site.register(list)