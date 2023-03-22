from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from.models import  message
from .serializers import MessagesSerialiser, MessagesSender
from authenticator.isAuth import AuthUser
from django.db.models import Q

# Create your views here.
data = {'status': True, 'status_code': 200, 'message': 'success'}
err404 = {'status': False, 'status_code': 404, 'message': 'error not found'}
err401 = {'status': False, 'status_code': 401, 'message': 'invalid user'}
errInput = {'status': False, 'status_code': 401, 'message': 'invalid data'}


class MessagePageView(APIView):
    def get(self, request, page):
        if AuthUser(request):
            limit = page*16
            messages = message.objects.filter(Q(sender = request.user) | Q(receiver = request.user)).order_by("-date_time")
            msg_lists = []
            for x in messages:
                if len(msg_lists) == 0:
                    msg_lists.append(x)
                else:
                    already  = False
                    for y in msg_lists:
                        if y.id == x.id:
                            already = True
                        else:
                            pass

                    if already == True:
                        msg_lists.append(x)
            
            c = MessagesSerialiser(msg_lists[int(limit)-16:int(limit)], many=True)
            for i in c.data:
                i['username'] = i['receiver'] if i['sender'] == request.user.username else i['sender']
                i['sender_full_name'] = Profile.objects.get(user = User.objects.get(username = i['sender'])).name
                i['receiver_full_name'] = Profile.objects.get(user = User.objects.get(username = i['receiver'])).name
                i['user_full_name'] = Profile.objects.get(user = User.objects.get(username = i['username'])).name
                i['user_avatar'] = ProfileSerializer(Profile.objects.get(user = User.objects.get(username = i['username']))).data['profileimg']
                if i['sender'] == request.user.username:
                    i['message_body'] = f"You: {i['message_body']}"
            has_more_page = False
            if len(c.data) == 16:
                has_more_page = True

            data['hasMorePage'] = has_more_page
            data['data'] = c.data
            return JsonResponse(data)
        
        return JsonResponse(err401)
        
    def post(self, request, page):
        pass

class GetMessageView(APIView):

    def get(self, request, pk, page):
        if AuthUser(request):
            page = page*16
            try:
                pk = User.objects.get(username = pk)
            except User.DoesNotExist:
                return Response(err404)
            
            messages = message.objects.filter(Q(sender = request.user, receiver = pk) | Q(sender = pk, receiver = request.user)).order_by("-date_time")
            c = MessagesSerialiser(messages[int(page)-16: int(page)], many = True)
            for i in c.data:
                i['username'] = i['receiver'] if i['sender'] == request.user.username else i['sender']
                i['sender_full_name'] = Profile.objects.get(user = User.objects.get(username = i['sender'])).name
                i['receiver_full_name'] = Profile.objects.get(user = User.objects.get(username = i['receiver'])).name
                i['user_full_name'] = Profile.objects.get(user = User.objects.get(username = i['username'])).name
                i['user_avatar'] = ProfileSerializer(Profile.objects.get(user = User.objects.get(username = i['username']))).data['profileimg']
                i['type'] = 2 if i['receiver'] == request.user.username else 1

            if len(c.data) == 16:
                has_more_page = True
            else:
                has_more_page = False
            data['hasMorePage'] = has_more_page
            data['data'] = c.data
            return Response(data)
        return Response(err401)


class sendmessage(APIView):
    self_err = {'status': False, 'status_code': 404,'message': 'You can\'t send message to your self'}
    error404 = {'status': False, 'status_code': 404,'message': 'User not exists'}
    error400 = {'status': False, 'status_code': 400,'message': 'Invalid user'}
    success = {'status': True, 'status_code': 200, 'message': 'send success'}
    def RETURN(self, id, request):
        msg = MessagesSerialiser(message.objects.get(id = id))
        username = msg.data['receiver'] if msg.data['sender'] == request.user.username else msg.data['sender']
        self.success['data'] = msg.data
        self.success['data']['username'] = username
        self.success['data']['sender_full_name'] = Profile.objects.get(user = User.objects.get(username = msg.data['sender'])).name
        self.success['data']['receiver_full_name'] = Profile.objects.get(user = User.objects.get(username = msg.data['receiver'])).name
        self.success['data']['user_full_name'] = Profile.objects.get(user = User.objects.get(username = username)).name
        self.success['data']['user_avatar'] = ProfileSerializer(Profile.objects.get(user = User.objects.get(username = username))).data['profileimg']
        self.success['data']['type'] = 2 if username == request.user.username else 1
        return Response(self.success)
    
    def post(self, request):
        if request.user.is_authenticated:
            sender_model = User.objects.get(username=request.user)
            try:
                receiver_model = User.objects.filter(username=request.data['receiver']).first()
                if receiver_model == sender_model:
                    return Response(self.self_err)
            except User.DoesNotExist:
                return Response(self.err404)
  
            data={
                'sender': sender_model.id,
                'receiver': receiver_model.id,
                'message_body': request.data['message']}

            serializers = MessagesSender(data=data)
            if serializers.is_valid(raise_exception=True):
                serializers.save()
                return self.RETURN(serializers.data['id'], request)
            return Response(errInput)
        
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
            self.success['length'] = len(serialiser.data)
            self.success['data'] = serialiser.data
            return Response(self.success)
        return Response(self.error400)
    
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
    err404 = {'status': False, 'status_code': 401,'message': 'message not exists'}
    error400 = {'status': False, 'status_code': 400,'message': 'Invalid user'}
    def get(self, request, message_id):
        if request.user.is_authenticated:
            try:
                msg = message.objects.get(id = message_id)
            except message.DoesNotExist:
                return Response(self.err404)
            
            msg.seen = True
            msg.save()
            return Response({"status": True, "status_code": 200, "message": "message seen"})
        
        return Response(self.error400)




