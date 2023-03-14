import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from users.models import OnlineUser

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		
		self.user = self.scope['user']
		if self.user.is_authenticated:
			print("connection from: ", self.user)
			self.user = await database_sync_to_async(self.getUser)(self.user.id)
			await self.accept()

	async def disconnect(self, close_code):
		print("connection close:", close_code)


	async def receive(self, text_data):
		print(text_data)

	async def chat_message(self, event):
		message = event['message']
		await self.send(text_data=json.dumps(message))
