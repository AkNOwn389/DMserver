from rest_framework import serializers
from .models import Images, Post, LikePost

class ImagesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Images
    fields = ['image']

class PostUploader(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = ['id','creator', 'creator_full_name', 'videos_url', 'images_url', 'title', 'description', 'created_at','NoOflike', 'NoOfcomment', 'media_type']

class PostSerializer(serializers.ModelSerializer):
  creator = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )
  class Meta:
    model = Post
    fields = ['id','creator', 'creator_full_name', 'title', 'description', 'created_at','NoOflike', 'NoOfcomment', 'media_type']

  def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["image_url"] = ImagesSerializer(instance.images_url.all(), many=True).data
        rep["videos_url"] = ImagesSerializer(instance.videos_url.all(), many=True).data
        return rep

class LikesPostSerializer(serializers.ModelSerializer):
  class Meta:
    model = LikePost
    fields = ['post_id', 'username']