from django.contrib import admin
from .models import Post, Postcomment
# Register your models here.
lists = [
    Post,
    Postcomment
]
admin.site.register(lists)
