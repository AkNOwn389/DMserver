from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
from.models import ChatRoom, ChatMessage
from .serializers import ChatMessageSender, ChatMessageSerializer
# Create your views here.

class sendmessage(APIView):
    def post(self, request):
        sender_model = User.objects.filter(username=request.user).first()
        receiver_model = User.objects.filter(username=request.data['receiver']).first()
        if receiver_model is None:
            return Response({'status': False, 'status_code': 404,'message': 'User not exists'})
        elif receiver_model == sender_model:
            return Response({'status': False, 'status_code': 404,'message': 'You can\'t send message to your self'})
        lists = ChatRoom.objects.filter(users = receiver_model)
        chatid = None
        for x in lists:
            if sender_model in x.users.all():
                chatid = x.chat_id
        if chatid is None:
            s = ChatRoom.objects.create()
            s.users.add(sender_model, receiver_model)
            s.save()
            chatid = s.chat_id
        data={
            'messageid': chatid,
            'msg_sender': sender_model.id,
            'msg_receiver': receiver_model.id,
            'body': request.data['message']}

        serializers = ChatMessageSender(data=data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return JsonResponse({'status': True,
            'message': 'send success'})
        return JsonResponse({'status': False, 'message': 'invalid data'})

class get_message(APIView):
    def get(self, request):
        all_message_receive = ChatMessage.objects.filter(msg_receiver_id=request.user.id)
        all_message_send = ChatMessage.objects.filter(msg_sender_id=request.user.id)
        serialize_msg_receive = ChatMessageSerializer(all_message_receive, many=True)
        serialize_msg_send = ChatMessageSerializer(all_message_send, many=True)


        return JsonResponse({'status': True, 'message': 'success', 'message_send': serialize_msg_send.data, 'message_receive': serialize_msg_receive.data})
