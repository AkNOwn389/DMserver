from django.contrib import admin
from .models import Post, Comment, LikePost, Image
# Register your models here.
lists = [
    Post,
    Comment,
    LikePost,
    Image
]
admin.site.register(lists)
