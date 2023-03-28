from django.contrib.auth.models import User
from rest_framework.views import APIView
from .models import MyNotification
from rest_framework.response import Response
from .serializers import NotificationSerializer
from posts.models import Post
from profiles.models import Profile
from chats.models import message
from django.db.models import Q, F
from users.models import FollowerCount


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
    

class Seen(APIView):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                notif = MyNotification.objects.get(user = request.user, subject_id = id)
                notif.seen = True
                notif.save()
                success['message'] = 'success'
                Response(success)
            except MyNotification.DoesNotExist:
                err_404['message'] = "doest not exists"
                Response(err_404)

        err_401['message'] = 'invalid cridential'
        Response(err_401)

class NotificationBadgeView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            notif = MyNotification.objects.filter(user = request.user, seen = False)
            success['message'] = 'success'
            success['lenght'] = len(notif) if len(notif) < 100 else 99
            return Response(success)
        err_401['message'] = 'invalid cridential'
        return Response(err_401)
        
class ChatBadge(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            notif = message.objects.filter(receiver = request.user, seen = False)
            success['message'] = 'success'
            success['lenght'] = len(notif) if len(notif) < 100 else 99
            return Response(success)
        err_401['message'] = 'invalid cridential'
        return Response(err_401)
    
class MyNotificationView(APIView):
    def get(self, request, page):
        page = page*16
        if request.user.is_authenticated:
            notifications = MyNotification.objects.filter(user = request.user, seen = False).order_by("-date")
            if notifications is None:
                success['data'] = []
                return Response(success)
            serializer = NotificationSerializer(notifications[int(page)-16:int(page)], many = True)
            for i in serializer.data:
                del i['subjectUser']
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
    
        

    
class LikeNotificationView:
    def saveLike(ako, postId):
        name = Profile.objects.get(user = ako).name
        if name == "" or name == None:
            name = ako.username
        creator = User.objects.get(username = Post.objects.get(id = postId).creator)
        if creator.username == ako.username:
            name = "You"
        try:
            notif = MyNotification.objects.get(user = creator, subject_id = postId, notifType =2)
            if not ako in notif.subjectUser.all():
                notif.subjectUser.add(ako)
            notif.title = f"{name} and {str(len(notif.subjectUser.all()) -1)} others likes your posts"
            notif.save()
            return
        except MyNotification.DoesNotExist:
            notif = MyNotification.objects.create(user = creator, subject_id = postId, title = f"{name} like your posts", description = "", notifType = 2)
            notif.subjectUser.add(ako)
            notif.save()
            return
    
    def deleteNotification(ako, postId):
        creator = User.objects.get(username = Post.objects.get(id = postId).creator)
        try:
            notif = MyNotification.objects.get(user = creator, subject_id = postId, description = "", notifType = 2)
            if ako in notif.subjectUser.all():
                notif.subjectUser.remove(ako)
                if len(notif.subjectUser.all()) == 0:
                    notif.delete()
                else:
                    name = notif.subjectUser.all()[0].username
                    if name == creator.username:
                        name = "You"
                    if len(notif.subjectUser.all()) == 1:
                        
                        notif.title = f"{name} likes your posts"
                    else:
                        notif.title = f"{name} and {str(len(notif.subjectUser.all()) -1)} likes your posts"
                    notif.save()
            return
        except MyNotification.DoesNotExist:
            pass

        return
    
class CommentNotificationView:
    def Notify(post_id, request):
        name = Profile.objects.get(user = request.user).name
        if name == "" or name == None:
            name = request.user.username
        creator = User.objects.get(username = Post.objects.get(id = post_id).creator)
        if creator == request.user:
            return
        
        try:
            notif = MyNotification.objects.get(user = creator, subject_id = post_id, notifType = 3)
            notif.title = f"{name} and {str(len(notif.subjectUser.all()))} others commented on your posts"
            if not request.user in notif.subjectUser.all():
                notif.subjectUser.add(request.user)
            
            notif.seen = False
            notif.save()

        except MyNotification.DoesNotExist:
            notif = MyNotification.objects.create(user = creator, subject_id = post_id, title = f"{name} commented on your posts", description = "", notifType = 3)
            notif.subjectUser.add(request.user)
            notif.save()
        return
    
class FollowNotificationView:
    def Notify(request, following):
        name = Profile.objects.get(user = request.user).name
        if name == "" or name == None:
            name = request.user.username

        if FollowerCount.objects.filter(follower = following, user = request.user).first():
            if not MyNotification.objects.filter(user = following, subjectUser__pk = request.user.id, title = f"{str(name)} and you are now friends.").first():
                notif = MyNotification.objects.create(user = following, title = f"{str(name)} and you are now friends.", description = str(name)+" followed you", notifType = 1, subject_id = request.user.username)
                notif.subjectUser.add(request.user)
                notif.save()
        else:
            if not MyNotification.objects.filter(user = following, subjectUser__pk = request.user.id, title = f"{str(name)} followed you.").first():
                MyNotification.objects.create(user = following, subjectUser = request.user, title = f"{str(name)} followed you.", description = str(name)+" followed you", notifType = 1, subject_id = request.user.username).save()

    def deleteNotif(request, following):
        name = Profile.objects.get(user = request.user).name
        if name == "" or name == None:
            name = request.user.username
        try:
            note = MyNotification.objects.get(user = following, subjectUser__pk = request.user.id, title = f"{str(name)} followed you.", description = str(name)+" followed you")
            note.delete()
        except MyNotification.DoesNotExist:
            pass
        try:
            note = MyNotification.objects.get(user = following, subjectUser__pk = request.user.id, title = f"{str(name)} and you are now friends.", description = str(name)+" followed you")
            note.delete()
        except MyNotification.DoesNotExist:
            pass
        return