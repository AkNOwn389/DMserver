import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import ChatRoom, ChatMessage
from users.models import OnlineUser

class Test(AsyncWebsocketConsumer):
	async def connect(self):
		return {"message": "you are connected"}

class ChatConsumer(AsyncWebsocketConsumer):
	def getUser(self, userId):
		return User.objects.get(id=userId)

	def getOnlineUsers(self):
		onlineUsers = OnlineUser.objects.all()
		return [onlineUser.user.id for onlineUser in onlineUsers]

	def addOnlineUser(self, user):
		try:
			OnlineUser.objects.create(user=user)
			
		except:
			pass

	def deleteOnlineUser(self, user):
		try:
			OnlineUser.objects.get(user=user).delete()
		except:
			pass

	def saveMessage(self, message, userId, roomId):
		userObj = User.objects.get(id=userId)
		chatObj = ChatRoom.objects.get(roomId=roomId)
		chatMessageObj = ChatMessage.objects.create(
			chat=chatObj, user=userObj, message=message
		)
		return {
			'action': 'message',
			'user': userId,
			'roomId': roomId,
			'message': message,
			'userImage': userObj.image.url,
			'userName': userObj.first_name + " " + userObj.last_name,
			'timestamp': str(chatMessageObj.timestamp)
		}

	async def sendOnlineUserList(self):
		onlineUserList = await database_sync_to_async(self.getOnlineUsers)()
		chatMessage = {
			'type': 'chat_message',
			'message': {
				'action': 'onlineUser',
				'userList': onlineUserList
			}
		}
		await self.channel_layer.group_send('onlineUser', chatMessage)

	async def connect(self):
		self.user = self.scope['user']
		if self.user.is_authenticated:
			self.user = await database_sync_to_async(self.getUser)(self.user.id)
			await database_sync_to_async(self.addOnlineUser)(self.user)
			await self.accept()

	async def disconnect(self, close_code):
		await database_sync_to_async(self.deleteOnlineUser)(self.user)


	async def receive(self, text_data):
		print(text_data)

	async def chat_message(self, event):
		message = event['message']
		await self.send(text_data=json.dumps(message))
