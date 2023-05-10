from rest_framework import serializers
from posts.serializers import ImagesSerializer, VideoSerializer
from profiles.serializers import ProfileSerializer
from profiles.models import Profile

from .models import Comment, LikeComment

class PostCommentSerializer(serializers.ModelSerializer):
  user = serializers.SlugRelatedField(
    read_only = True,
    slug_field = "username"
  )
  class Meta:
    model = Comment
    fields = ['id', 'post_id', 'image', 'video', 'avatar', 'user', 'comments', 'created', 'comment_type', 'NoOflike']
  
  def to_representation(self, instance):
    rep = super().to_representation(instance)
    reactionList = {"Like":len(LikeComment.objects.filter(commentId = instance.id, reactionType = "T")),
                    "Love":len(LikeComment.objects.filter(commentId = instance.id, reactionType = "L")),
                    "Happy":len(LikeComment.objects.filter(commentId = instance.id, reactionType = "H")),
                    "Sad":len(LikeComment.objects.filter(commentId = instance.id, reactionType = "S")),
                    "Wow":len(LikeComment.objects.filter(commentId = instance.id, reactionType = "W")),
                    "Angry":len(LikeComment.objects.filter(commentId = instance.id, reactionType = "A"))}
    profile = ProfileSerializer(Profile.objects.get(user = instance.user)).data
    rep['avatar'] = profile['profileimg']
    rep["image"] = ImagesSerializer(instance.image.all(), many=True).data
    rep["video"] = VideoSerializer(instance.video.all(), many=True).data
    rep['reactions'] = reactionList
    return rep
  