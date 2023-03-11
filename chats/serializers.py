from rest_framework import serializers
from .models import ChatMessage, ChatRoom, RoomMessage, Room




class ChatMessageSerializer(serializers.ModelSerializer):
  msg_sender = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )
  msg_receiver = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )
  class Meta:
    model = ChatMessage
    fields = ['msg_sender', 'msg_receiver', 'body', 'created_time', 'created_at', 'seen']

class ChatMessageSender(serializers.ModelSerializer):
  class Meta:
    model = ChatMessage
    fields = ['messageid', 'msg_sender', 'msg_receiver', 'body', 'created_time', 'created_at', 'seen']


class RoomMessageSerializer(serializers.ModelSerializer):
  class Meta:
    model = RoomMessage
    fields = ['room', 'msg_sender', 'body']