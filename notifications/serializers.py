from .models import MyNotification
from rest_framework import serializers
from django.contrib.auth.models import User
from users.serializers import UserSerializer
from profiles.serializers import ProfileSerializer
from profiles.models import Profile
from posts.models import Post
from time_.get_time import getStringTime
from posts.serializers import PostSerializer


class NotificationSerializer(serializers.ModelSerializer):
    userToNotify = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    subjectUser = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        many=True,
        slug_field="username")

    class Meta:
        model = MyNotification
        fields = ['id',
                  'userToNotify',
                  'subjectUser',
                  'subjectPostsId',
                  'title',
                  'description',
                  'notifType',
                  'seen',
                  'date']
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        profile = ProfileSerializer(Profile.objects.get(user=User.objects.get(username=instance.subjectUser.all()[0]))).data
        rep['subjectImage'] = profile['profileimg']
        rep['subjectFullName'] = profile['name']
        rep['subjectUserName'] = rep['subjectUser'][0]
        rep['display_date'] = getStringTime(rep['date'])
        return rep

