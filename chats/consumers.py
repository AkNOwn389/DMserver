import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from users.models import OnlineUser
from .models import  PrivateRoom
from django.db.models import Q
from .db_operations import get_user_by_id, get_user_by_username, mark_message_as_read
from .errors import ErrorTypes
from .models import message as UserMessage
from .message_types import MessageTypeFileMessage, MessageTypeMessageRead, MessageTypes, MessageTypeTextMessage, Optional, OutgoingEventIsTyping, OutgoingEventMessageIdCreated,OutgoingEventMessageRead, OutgoingEventNewFileMessage, OutgoingEventNewTextMessage, OutgoingEventNewUnreadCount, OutgoingEventStoppedTyping, OutgoingEventWentOffline, OutgoingEventWentOnline

class ChatConsumer(AsyncWebsocketConsumer):

	def SocksUser(self, user, chatMate):
		try:
			PrivateRoom.objects.filter(user = user).delete()
		except PrivateRoom.DoesNotExist:
			pass
		try:
			PrivateRoom.objects.create(user = user, connected_to = User.objects.get(username = chatMate)).save()
			self.connected = True
		except User.DoesNotExist:
			self.connected = False
		except:
			self.connected = False

	async def connect(self):
		self.user = self.scope['user']
		self.chatMate = self.scope['url_route']['kwargs']['user']
		
		if self.user.is_authenticated:
			print("connection from: ", self.user)
			print("connected in: ", self.chatMate)
			await database_sync_to_async(self.SocksUser)(self.user, self.chatMate)
			if self.connected == True:
				await self.accept()
				text = {
					'status': True,
					'status_code': 200,
					'message': 'connected'
				}
				await self.send(text_data = json.dumps(text))
				return
			print("Not Connected")
		

	async def disconnect(self, close_code):
		print("connection close:", close_code)


	async def receive(self, text_data):
		data = json.loads(text_data)


	async def chat_message(self, event):
		message = event['message']
		await self.send(text_data=json.dumps(message))
