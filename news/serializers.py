from rest_framework import serializers
from .models import News
from posts.models import LikePost


class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'avatar', 'title', 'news_id', 'name', 'author', 'description', 'url', 'urlToImage', 'publishedAt', 'content', 'noOfLike', 'noOfComment', 'noOfShare', 'news_type']
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        reactionList = {"Like":len(LikePost.objects.filter(post_id = instance.id, reactionType = "T")),
                        "Love":len(LikePost.objects.filter(post_id = instance.id, reactionType = "L")),
                        "Happy":len(LikePost.objects.filter(post_id = instance.id, reactionType = "H")),
                        "Sad":len(LikePost.objects.filter(post_id = instance.id, reactionType = "S")),
                        "Wow":len(LikePost.objects.filter(post_id = instance.id, reactionType = "W")),
                        "Angry":len(LikePost.objects.filter(post_id = instance.id, reactionType = "A"))}
        rep['reactions'] = reactionList
        return rep