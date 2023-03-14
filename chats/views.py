from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
from.models import singleOneToOneRoom, message
from .serializers import MessagesSerialiser
# Create your views here.

class MessagePageView(APIView):
    def get(self, request, page):
        limit = page*8
        a = []
        b = singleOneToOneRoom.objects.filter(users = request.user)
        for x in b:
            y = message.objects.filter(messageid=x.chat_id).last()
            a.append(y)
        a.reverse()
        c = MessagesSerialiser(a[int(limit)-8:int(limit)], many=True)
        has_more_page = False
        if len(c.data) == 8:
            has_more_page = True
        return JsonResponse({'status': True, 'status_code': 200, 'message': 'beta test', 'hasMorePage': has_more_page, 'data': c.data})
    def post(self, request, page):
        pass
"""
class sendmessage(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            sender_model = User.objects.get(user=request.user)
            try:
                receiver_model = User.objects.filter(username=request.data['receiver']).first()
                if receiver_model == sender_model:
                    return Response({'status': False, 'status_code': 404,'message': 'You can\'t send message to your self'})
            except User.DoesNotExist:
                return Response({'status': False, 'status_code': 404,'message': 'User not exists'})
  
            
            lists = singleOneToOneRoom.objects.filter(users = receiver_model)
            chatid = None
            for x in lists:
                if sender_model in x.users.all():
                    chatid = x.chat_id
            if chatid is None:
                s = singleOneToOneRoom.objects.create()
                s.users.add(sender_model, receiver_model)
                s.save()
                chatid = s.chat_id
            data={
                'room': chatid,
                'msg_sender': sender_model.id,
                'msg_receiver': receiver_model.id,
                'body': request.data['message']}

            serializers = messagesSender(data=data)
            if serializers.is_valid(raise_exception=True):
                serializers.save()
                return JsonResponse({'status': True,
                'message': 'send success'})
            return JsonResponse({'status': False, 'message': 'invalid data'})

class get_message(APIView):
    def get(self, request):
        all_message_receive = messages.objects.filter(msg_receiver_id=request.user.id)
        all_message_send = messages.objects.filter(msg_sender_id=request.user.id)
        serialize_msg_receive = messagesSerializer(all_message_receive, many=True)
        serialize_msg_send = messagesSerializer(all_message_send, many=True)


        return JsonResponse({'status': True, 'message': 'success', 'message_send': serialize_msg_send.data, 'message_receive': serialize_msg_receive.data})
"""