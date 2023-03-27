from django.contrib.auth.models import User
from rest_framework.views import APIView
from .models import MyNotification
from rest_framework.response import Response
from .serializers import NotificationSerializer
from django.db.models import Q, F


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

class Notify(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            notifications = MyNotification.objects.filter(user = request.user, seen = False).order_by("-date")
            if notifications is None:
                success['data'] = []
                return Response(success)
            
            serializer = NotificationSerializer(notifications, many = True)
            success['message'] = "success"
            success['data'] = serializer.data
            return Response(success)
        err_401['message'] = "invalid user"
        return Response(err_401)
    
class MyNotificationView(APIView):

    def getLikesNotif(self, request):
        post = []
        notif = MyNotification.objects.filter(user = request.user, notifType=2)
        serializer = NotificationSerializer(notif, many = True)
        for i in serializer.data:
            if not len(post) == 0:
                already = False
                for x in post:
                    if x['subject_id'] == str(i['subject_id']):
                        already = True
                    
                if already == False:
                    post.append(i)
            else:
                
                post.append(i)

        notif = []
        for i in post:
            
            others = MyNotification.objects.filter(subject_id = i['subject_id'], notifType = 2).order_by('-date')
            if len(others) == 1:
                notif.append(others)
            else:
                first = MyNotification.objects.filter(subject_id = i['subject_id'], notifType = 2).order_by('-date').first()
                if str(first.subjectUser) == str(request.user):
                    name = "You"
                else:
                    name = first.subjectUser 
                first.title = f"{str(name)} and {str(len(others) -1)} others likes your posts"
                notif.append(first)
        return notif

      

    def get(self, request, page):
        page = page*16
        if request.user.is_authenticated:
            likeNotif = self.getLikesNotif(request=request)
            notifications = MyNotification.objects.filter(Q(user = request.user, notifType = 1) | Q(user = request.user, notifType = 3)).order_by("-date")
            if notifications is None:
                success['data'] = []
                return Response(success)
            serializer = NotificationSerializer(notifications[int(page)-16:int(page)], many = True)
            if len(serializer.data) == 16:
                hasMorePage = True
            else:
                hasMorePage = False
            
            success['hasMorePage'] = bool(hasMorePage)
            success['message'] = "success"
            success['data'] = serializer.data
            return Response(success)
        err_401['message'] = "invalid user"
        return Response(err_401)