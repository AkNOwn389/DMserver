from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FollowerCount




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