from rest_framework import serializers
from profiles.models import Profile
from posts.serializers import ImagesSerializer
from .models import RecentSearch
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
  user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )
  class Meta:
    model = Profile
    fields = ['user', 'profileimg', 'bgimg', 'bio', 'location', 'name', 'interested', 'gender', 'school', 'works']
  def to_representation(self, instance):
    rep = super().to_representation(instance)
    rep['id'] = User.objects.get(username = instance.user).id
    rep["hobby"] = ImagesSerializer(instance.hobby.all(), many=True).data
    return rep
  
class EditProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ['user_id', 'profileimg', 'bgimg', 'bio', 'location', 'name']

class RecentSearchSerializer(serializers.ModelSerializer):
  user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )
  searcher = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )
  class Meta:
    model = RecentSearch
    fields = ["user", "searcher", "date_search"]