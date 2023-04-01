from rest_framework import serializers
from .models import Image, Videos,  Post, LikePost, Comment

class ImagesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Image
    fields = ['id', 'image', 'noOfComment', 'noOfLike']

class VideoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Videos
    fields = ['id', 'video', 'noOfComment', 'noOfLike']

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
    fields = ['id','creator', 'creator_full_name', 'title', 'perma_link',  'description', 'created_at','NoOflike', 'NoOfcomment', 'media_type', 'status']


  def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["image_url"] = ImagesSerializer(instance.images_url.all(), many=True).data
        rep["videos_url"] = ImagesSerializer(instance.videos_url.all(), many=True).data
        return rep

class LikesPostSerializer(serializers.ModelSerializer):
  class Meta:
    model = LikePost
    fields = ['post_id', 'username']

class PostCommentSerializer(serializers.ModelSerializer):
  user = serializers.SlugRelatedField(
    read_only = True,
    slug_field = "username"
  )
  class Meta:
    model = Comment
    fields = ['id', 'post_id', 'image', 'avatar', 'user', 'comments', 'created', 'type']