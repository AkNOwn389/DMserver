from rest_framework import serializers
from .models import Image, Videos,  Post, LikePost
from django.contrib.auth.models import User
import cloudinary
from time_.get_time import getStringTime
class ImagesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Image
    fields = ['id', 'url', 'thumbnail', 'url_w1000', 'url_w250', 'NoOfcomment', 'NoOflike', 'width', 'height']
  
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

class VideoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Videos
    fields = ['id', 'original', 'url_w1000', 'url_w500', 'url_w250', 'thumbnail', 'playback_url', 'width', 'height']

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

class PostUploader(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = ['id','creator', 'creator_full_name', 'videos_url', 'images_url', 'title', 'description', 'created_at','NoOflike', 'NoOfcomment', 'media_type', 'privacy']

class PostSerializer(serializers.ModelSerializer):
  creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )
  class Meta:
    model = Post
    fields = ['id','creator', 'creator_full_name', 'title', 'perma_link',  'description', 'created_at', 'NoOflike', 'NoOfcomment', 'media_type', 'status', 'privacy']


  def to_representation(self, instance):
        rep = super().to_representation(instance)
        reactionList = {"Like":len(LikePost.objects.filter(post_id = instance.id, reactionType = "T")),
                        "Love":len(LikePost.objects.filter(post_id = instance.id, reactionType = "L")),
                        "Happy":len(LikePost.objects.filter(post_id = instance.id, reactionType = "H")),
                        "Sad":len(LikePost.objects.filter(post_id = instance.id, reactionType = "S")),
                        "Wow":len(LikePost.objects.filter(post_id = instance.id, reactionType = "W")),
                        "Angry":len(LikePost.objects.filter(post_id = instance.id, reactionType = "A"))}
        rep['reactions'] = reactionList
        rep["image_url"] = ImagesSerializer(instance.images_url.all(), many=True).data
        rep["videos_url"] = VideoSerializer(instance.videos_url.all(), many=True).data
        rep['created'] = instance.created_at
        return rep

class LikesPostSerializer(serializers.ModelSerializer):
  class Meta:
    model = LikePost
    fields = ['post_id', 'username', 'reactionType']
  def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['reactionType'] = instance.get_reactionType_display()
        return rep

from profiles.serializers import ProfileSerializer, Profile