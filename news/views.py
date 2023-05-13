from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import AbstractBaseUser
from .models import News
from rest_framework.response import Response
from .serializers import NewsSerializers
from posts.models import Post, LikePost
from time_.get_time import getStringTime
from posts.serializers import LikesPostSerializer
import re
# Create your views here.

class GetNew(APIView):
    def get(self, request, page):
        user:AbstractBaseUser = request.user
        if user.is_authenticated:
            page = page*16
            news = News.objects.all().order_by("-publishedAt")
            serialiser = NewsSerializers(news[int(page) - 16:int(page)], many = True)
            for i in serialiser.data:
                if LikePost.objects.filter(post_id=i['id'], username=request.user).exists():
                    i['is_like'] = True
                    i['reactionType'] = LikesPostSerializer(LikePost.objects.filter(post_id=i['id'], username=request.user).first()).data['reactionType']
                else:
                    i['is_like'] = False
                i['content'] = i['content'][ :int ( len(i['content'])) - 13]
                i['publishedAt'] = getStringTime(i['publishedAt'])
            return Response({
                "hasMorePage": True if len(serialiser.data) >= 16 else False,
                "status":True,
                "status_code":200,
                "message": "success",
                "data": serialiser.data
            })
        else:
            return Response({
                "status":False,
                "status_code": 403,
                "message": "invalid user"
            })
