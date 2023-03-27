from .models import MyNotification
from rest_framework import serializers

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )
    subjectUser = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )
    class Meta:
        model = MyNotification
        fields = ['id', 'user', 'subjectUser', 'subject_id', 'title', 'description', 'notifType', 'seen', 'date']