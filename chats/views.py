from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from.models import  message
from .serializers import MessagesSerialiser
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
                pk = User.objects.get(Q(username = pk) | Q(id = pk))
            except User.DoesNotExist:
                return Response(err404)
            
            messages = message.objects.filter(
                Q(sender = request.user, receiver = pk
                ) | Q(sender = pk, receiver = request.user
                )).order_by("-timeStamp")
            
            c = MessagesSerialiser(messages, many = True)
            if len(c.data) == 16:
                has_more_page = True
            data['hasMorePage'] = has_more_page
            data['data'] = c.data
            return Response(data)
        return Response(err401)


class sendmessage(APIView):
    self_err = {'status': False, 'status_code': 404,'message': 'You can\'t send message to your self'}
    error404 = {'status': False, 'status_code': 404,'message': 'User not exists'}
    success = {'status': True, 'status_code': 200, 'message': 'send success'}

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

            serializers = MessagesSerialiser(data=data)
            if serializers.is_valid(raise_exception=True):
                serializers.save()
                return Response(self.success)
            return Response(errInput)
        
        return Response(self.error404)

