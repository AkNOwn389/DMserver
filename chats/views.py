from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from.models import PrivateMessage as message
from .serializers import MessagesSerialiser, MessagesSender
from authenticator.isAuth import AuthUser
from django.db.models import Q
from .managers import MessageManager
from django.contrib.auth.models import AbstractBaseUser
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# Create your views here.
data = {'status': True, 'status_code': 200, 'message': 'success'}
success = {"status": True, "status_code": 200}
err_400 = {"status": False, "status_code": 400}
err_401 = {"status": False, "status_code": 401}
err_402 = {"status": False, "status_code": 402}
err_403 = {"status": False, "status_code": 403}
err_404 = {"status": False, "status_code": 404}
err_405 = {"status": False, "status_code": 405}
err_406 = {"status": False, "status_code": 406}
err_407 = {"status": False, "status_code": 407}
err_408 = {"status": False, "status_code": 408}
err_409 = {"status": False, "status_code": 409}
err_410 = {"status": False, "status_code": 410}
err_411 = {"status": False, "status_code": 411}
err_412 = {"status": False, "status_code": 412}
err_413 = {"status": False, "status_code": 413}
err_414 = {"status": False, "status_code": 414}
err_415 = {"status": False, "status_code": 415}
err_416 = {"status": False, "status_code": 416}


class MessagePageView(APIView):
    def get(self, request, page):
        if AuthUser(request):
            limit = page*16
            user:AbstractBaseUser = request.user
            msg_lists = MessageManager().getMainPageView(user=user)
            c = MessagesSerialiser(msg_lists[int(limit)-16:int(limit)], many=True)
            for i in c.data:
                i['username'] = i['receiver'] if i['sender'] == user.username else i['sender']
                i['sender_full_name'] = Profile.objects.get(user = User.objects.get(username = i['sender'])).name
                i['receiver_full_name'] = Profile.objects.get(user = User.objects.get(username = i['receiver'])).name
                i['user_full_name'] = Profile.objects.get(user = User.objects.get(username = i['username'])).name
                i['user_avatar'] = ProfileSerializer(Profile.objects.get(user = User.objects.get(username = i['username']))).data['profileimg']
                i['message_lenght'] = len(message.objects.filter(sender = User.objects.get(username = i['username']), receiver = user))
                i['type'] = 1
                if i['sender'] == user.username:
                    i['message_body'] = f"You: {i['message_body']}"
            has_more_page = False
            if len(c.data) == 16:
                has_more_page = True

            data['hasMorePage'] = has_more_page
            data['data'] = c.data
            return JsonResponse(data)
        
        return JsonResponse(err_401)
        
    def post(self, request, page):
        pass

class GetMessageView(APIView):

    def get(self, request, pk, page):
        if AuthUser(request):
            page = page*16
            try:
                pk = User.objects.get(username = pk)
            except User.DoesNotExist:
                err_404['message'] = 'not found'
                return Response(err_404)
            
            messages = message.objects.filter(Q(sender = request.user, receiver = pk) | Q(sender = pk, receiver = request.user)).order_by("-date_time")
            c = MessagesSerialiser(messages[int(page)-16: int(page)], many = True)
            for i in c.data:
                i['username'] = i['receiver'] if i['sender'] == request.user.username else i['sender']
                i['sender_full_name'] = Profile.objects.get(user = User.objects.get(username = i['sender'])).name
                i['receiver_full_name'] = Profile.objects.get(user = User.objects.get(username = i['receiver'])).name
                i['user_full_name'] = Profile.objects.get(user = User.objects.get(username = i['username'])).name
                i['user_avatar'] = ProfileSerializer(Profile.objects.get(user = User.objects.get(username = i['sender']))).data['profileimg']
                i['type'] = 2 if i['receiver'] == request.user.username else 1
                i['me'] = True if i['sender'] == request.user.username else False

            if len(c.data) == 16:
                has_more_page = True
            else:
                has_more_page = False
            data['hasMorePage'] = has_more_page
            data['data'] = c.data
            return Response(data)
        return Response(err_401)


class sendmessage(APIView):
    self_err = {'status': False, 'status_code': 404,'message': 'You can\'t send message to your self'}
    error404 = {'status': False, 'status_code': 404,'message': 'User not exists'}
    error400 = {'status': False, 'status_code': 400,'message': 'Invalid user'}
    success = {'status': True, 'status_code': 200, 'message': 'send success'}
    
    def notify_new_message(self, event: dict, room: str) -> None:
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(room, event)
            return None
        except Exception as e:
            print(e)
    
    def RETURN(self, id, request):
        msg = MessagesSerialiser(message.objects.get(id = id))
        username = msg.data['receiver'] if msg.data['sender'] == request.user.username else msg.data['sender']
        self.success['data'] = msg.data
        self.success['data']['username'] = username
        self.success['data']['sender_full_name'] = Profile.objects.get(user = User.objects.get(username = msg.data['sender'])).name
        self.success['data']['receiver_full_name'] = Profile.objects.get(user = User.objects.get(username = msg.data['receiver'])).name
        self.success['data']['user_full_name'] = Profile.objects.get(user = User.objects.get(username = username)).name
        self.success['data']['user_avatar'] = ProfileSerializer(Profile.objects.get(user = User.objects.get(username = msg.data['sender']))).data['profileimg']
        self.success['data']['type'] = 2 if username == request.user.username else 1
        self.success['data']['me'] = True
        self.notify_new_message(event=success, room=f"room_{username}_chat_page")
        return Response(self.success)
     
    """
    channel_layer = get_channel_layer()

async_to_sync(channel_layer.group_add)(
    'room_name',
    'channel_name'
)
    """
    
    def post(self, request):
        if request.user.is_authenticated:
            sender_model = User.objects.get(username=request.user)
            try:
                receiver_model = User.objects.filter(username=request.data['receiver']).first()
                if receiver_model == sender_model:
                    return Response(self.self_err)
            except User.DoesNotExist:
                err_404['message'] = 'not found'
                return Response(err_404)
  
            data={
                'sender': sender_model.id,
                'receiver': receiver_model.id,
                'message_body': request.data['message']}

            serializers = MessagesSender(data=data)
            if serializers.is_valid(raise_exception=True):
                serializers.save()
                return self.RETURN(serializers.data['id'], request)
            
            err_404['message'] = 'not found'
            return Response(err_404)
        
        return Response(self.error400)

class Notify(APIView):
    self_err = {'status': False, 'status_code': 401,'message': 'invalid'}
    error400 = {'status': False, 'status_code': 400,'message': 'Invalid user'}
    success = {'status': True, 'status_code': 200, 'message': 'notify', 'data': []}
    def get(self, request):
        if request.user.is_authenticated:
            messages = message.objects.filter(receiver = request.user, seen = False).order_by("-date_time")
            if messages is None:
                self.success['message'] = "notify"
                self.success['data'] = []
                return JsonResponse(self.success)
            serialiser = MessagesSerialiser(messages, many = True)
            for msg in serialiser.data:
                username = msg['receiver'] if msg['sender'] == request.user.username else msg['sender']
                msg['username'] = username
                msg['sender_full_name'] = Profile.objects.get(user = User.objects.get(username = msg['sender'])).name
                msg['receiver_full_name'] = Profile.objects.get(user = User.objects.get(username = msg['receiver'])).name
                msg['user_full_name'] = Profile.objects.get(user = User.objects.get(username = username)).name
                msg['user_avatar'] = ProfileSerializer(Profile.objects.get(user = User.objects.get(username = username))).data['profileimg']
                msg['type'] = 2 if username == request.user.username else 1
                msg['me'] = False
            self.success['length'] = len(serialiser.data)
            self.success['data'] = serialiser.data
            return Response(self.success)
        return Response(self.error400)
    
class ChatListener(APIView):
    def get(self, request, user):
        if request.user.is_authenticated:
            try:
                user = User.objects.get(username = user)
            except User.DoesNotExist:
                err_404['message'] = 'user not found'
                return Response(err_404)
            messages = message.objects.filter(sender = user, receiver = request.user, seen = False).order_by("date_time")
            if len(messages) == 0:
                success['message'] = "none"
                success['data'] = []
                return JsonResponse(success)
            serializer = MessagesSerialiser(messages, many = True)
            for msg in serializer.data:
                username = msg['receiver'] if msg['sender'] == request.user.username else msg['sender']
                msg['username'] = username
                msg['sender_full_name'] = Profile.objects.get(user = User.objects.get(username = msg['sender'])).name
                msg['receiver_full_name'] = Profile.objects.get(user = User.objects.get(username = msg['receiver'])).name
                msg['user_full_name'] = Profile.objects.get(user = User.objects.get(username = username)).name
                msg['user_avatar'] = ProfileSerializer(Profile.objects.get(user = User.objects.get(username = username))).data['profileimg']
                msg['type'] = 1 if username == request.user.username else 2
                msg['me'] = False
            success['hasMorePage'] = False
            success['message'] = 'success'
            success['data'] = serializer.data
            return Response(success)

class DeleleMessage(APIView):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                chat = message.objects.get(sender = request.user, id = id)
                chat.message_body = 'deleted.'
                chat.is_delete = True
                chat.save()
            except message.DoesNotExist:
                err_404['message'] = "Not Found"
                return Response(err_404)
            success['message'] = "message deleted"
            return Response(success)
        err_401['message'] = "invalid user"
        return Response(err_401)

class MessageBadge(APIView):
    error400 = {'status': False, 'status_code': 400,'message': 'Invalid user'}
    err = {'status': False, 'status_code': 401,'message': 'invalid user'}
    def get(self, request):
        if request.user.is_authenticated:
            messages = message.objects.filter(receiver = request.user, seen = False).order_by("-date_time")
            if messages is None:
                Response({"status": True, "status_code": 200, "message": "success", "length": len(messages)})
        Response(self.error400)

class Seen(APIView):
    err404 = {'status': False, 'status_code': 404,'message': 'message not exists'}
    error401 = {'status': False, 'status_code': 401,'message': 'Invalid user'}
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                msg = message.objects.get(id = id, receiver = request.user)
            except message.DoesNotExist:
                return Response(self.err404)
            msg.seen = True
            msg.save()
            return Response({"status": True, "status_code": 200, "message": "message seen"})
        
        return Response(self.error401)




