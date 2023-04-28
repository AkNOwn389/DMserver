from rest_framework import serializers
from .models import News


class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'avatar', 'title', 'news_id', 'name', 'author', 'description', 'url', 'urlToImage', 'publishedAt', 'content', 'noOfLike', 'noOfComment', 'noOfShare', 'news_type']