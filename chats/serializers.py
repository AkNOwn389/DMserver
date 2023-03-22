from .models import message
from rest_framework import serializers

class MessagesSerialiser(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )
    receiver = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )
    class Meta:
        model = message
        fields = ['id', 'message_body', 'sender', 'receiver', 'date_time', 'seen', 'is_delete']

class MessagesSender(serializers.ModelSerializer):
    class Meta:
        model = message
        fields = ['id', 'message_body', 'sender', 'receiver', 'date_time', 'seen', 'is_delete']