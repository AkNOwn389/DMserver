from .models import MyNotification
from rest_framework import serializers
from django.contrib.auth.models import User

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )
    subjectUser = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        many=True,
        slug_field="username")
    
    class Meta:
        model = MyNotification
        fields = ['id', 'user', 'subjectUser', 'subject_id', 'title', 'description', 'notifType', 'seen', 'date']