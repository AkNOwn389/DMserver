from django.contrib import admin
from .models import Post, LikePost, Image
# Register your models here.
lists = [
    Post,
    LikePost,
    Image
]
admin.site.register(lists)
