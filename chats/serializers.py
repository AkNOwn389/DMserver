from .models import singleOneToOneRoom, message
from rest_framework import serializers

class PrivateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = singleOneToOneRoom
        fields = ['first_user', 'second_user']

class MessagesSerialiser(serializers.ModelSerializer):
    class Meta:
        model = message
        fields = ['room', 'message_body', 'sender', 'receiver', 'timeStamp', 'seen']