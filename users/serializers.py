from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FollowerCount, ChangePasswordHistory, OnlineUser
from profiles.serializers import ProfileSerializer
from profiles.models import Profile


class OnlineUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = OnlineUser
    fields = ['user']
  def to_representation(self, instance):
    user = User.objects.get(username = instance.user.username)
    profile = Profile.objects.get(user = user)
    serialize_profile = ProfileSerializer(profile).data
    rep = super().to_representation(instance)
    rep['id'] = rep['user']
    rep['username'] = user.username
    rep['avatar'] = serialize_profile['profileimg']
    rep['name'] = serialize_profile['name']
    del rep['user']
    return rep
  
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
    extra_kwargs = {
      "password": {
        "write_only": True
        }
    }

class FollowersCountSerializer(serializers.ModelSerializer):
  class Meta:
    model = FollowerCount
    fields = ['follower', 'user']
    
class ChangePasswordHistorySerializer(serializers.ModelSerializer):
  class Meta:
    model = ChangePasswordHistory
    fields = ['user', 'date', 'device', 'ip']