from optparse import Option
from typing import Union, Optional

from django.contrib.auth.models import User
from rest_framework.views import APIView
from .models import MyNotification
from rest_framework.response import Response
from .serializers import NotificationSerializer
from profiles.serializers import ProfileSerializer
from posts.serializers import PostSerializer
from posts.models import Post
from profiles.models import Profile
from chats.models import PrivateMessage as message
from django.db.models import Q, F
from users.models import FollowerCount
from time_.get_time import getStringTime
from django.http import HttpRequest
from .dbManager import getSeenNotification, getUnseenNotification, getAllNotification, pustNotifications, chatBadge, notifBadge, getOrCreateNotificationChannel, pushBadge
from django.contrib.auth.models import AbstractBaseUser

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
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            notifications = MyNotification.objects.filter(userToNotify=request.user, seen=False).order_by("-date")
            if notifications is None:
                success['data'] = []
                return Response(success)

            serializer = NotificationSerializer(notifications, many=True)
            success['message'] = "success"
            success['data'] = serializer.data
            return Response(success)
        err_401['message'] = "invalid user"
        return Response(err_401)


class Delete(APIView):
    success = {"status": True, "status_code": 200}

    def get(self, request: HttpRequest, id: str) -> Response:
        if request.user.is_authenticated:
            try:
                MyNotification.objects.get(userToNotify=request.user, id=id).delete()
                self.success['message'] = "success"
                return Response(self.success)
            except MyNotification.DoesNotExist:
                err_404['message'] = "doest not exists"
                return Response(err_404)

        err_401['message'] = 'invalid cridential'
        return Response(err_401)


class Seen(APIView):
    success = {"status": True, "status_code": 200}

    def get(self, request: HttpRequest, id: str) -> Response:
        if request.user.is_authenticated:
            try:
                notif = MyNotification.objects.get(userToNotify=request.user, id=id)
                if notif.seen:
                    self.success['message'] = "Already seen"
                    self.success['status'] = False
                    return Response(success)
                notif.seen = True
                notif.save()
                self.success['message'] = "success"
                pushBadge(creator=request.user)
                return Response(success)
            except MyNotification.DoesNotExist:
                err_404['message'] = "doest not exists"
                return Response(err_404)

        err_401['message'] = 'invalid cridential'
        return Response(err_401)


class NotificationBadgeView(APIView):
    def get(self, request: HttpRequest) -> Response:
        if request.user.is_authenticated:
            notif = MyNotification.objects.filter(userToNotify=request.user, seen=False)
            success['message'] = 'success'
            success['lenght'] = len(notif) if len(notif) < 100 else 99
            return Response(success)
        err_401['message'] = 'invalid cridential'
        return Response(err_401)


class ChatBadge(APIView):
    def get(self, request: HttpRequest) -> Response:
        if request.user.is_authenticated:
            notif = message.objects.filter(receiver=request.user, seen=False)
            success['message'] = 'success'
            success['lenght'] = len(notif) if len(notif) < 100 else 99
            return Response(success)
        err_401['message'] = 'invalid cridential'
        return Response(err_401)


def getTypeOneNotificationDetails(event: dict) -> Optional[Union[None, dict]]:
    try:
        profile = ProfileSerializer(Profile.objects.get(user=User.objects.get(username=event['subjectUser'][0]))).data
        event['subjectImage'] = profile['profileimg']
        event['subjectFullName'] = profile['name']
        event['subjectUserName'] = event['subjectUser'][0]
        event['display_date'] = getStringTime(event['date'])
        del event['subjectUser']
        return event
    except Exception as e:
        print(f"\044[1;91mError Log in getTypeOneNotificationDetails: {e}")
        return None


def getTypeTwoNotificationDetails(event: dict) -> Optional[Union[None, dict]]:
    try:
        profile = ProfileSerializer(Profile.objects.get(
            user=User.objects.get(username=event["subjectUser"][len(event['subjectUser']) - 1]))).data
        event['subjectImage'] = profile['profileimg']
        event['subjectFullName'] = profile['name']
        event['NoOfcomment'] = Post.objects.get(id=event['subjectPostsId']).NoOfComment
        event['NoOflike'] = Post.objects.get(id=event['subjectPostsId']).NoOflike
        event['display_date'] = getStringTime(event['date'])
        del event['subjectUser']
        return event
    except Exception as e:
        print(f"\044[1;91mError Log in getTypeTwoNotificationDetails: {e}")
        return None


def getTypeThreeNotificationDetails(event: dict) -> Optional[Union[None, dict]]:
    try:
        profile = ProfileSerializer(Profile.objects.get(
            user=User.objects.get(username=event["subjectUser"][len(event['subjectUser']) - 1]))).data
        posts: Post = Post.objects.get(id=event['subjectPostsId'])
        event['subjectImage'] = profile['profileimg']
        event['subjectFullName'] = profile['name']
        event['NoOfcomment'] = posts.NoOfComment
        event['NoOflike'] = posts.NoOflike
        event['reactedions'] = PostSerializer(posts).data['reactedions']
        event['display_date'] = getStringTime(event['date'])
        del event['subjectUser']
        return event
    except Exception as e:
        print(f"\044[1;91mError Log in getTypeThreeNotificationDetails: {e}")
        return None


class MyNotificationView(APIView):
    def get(self, request: HttpRequest, page: int):
        page = page * 30
        if request.user.is_authenticated:
            user: AbstractBaseUser = request.user
            notifications = getAllNotification(user=user)
            if notifications is None:
                success['data'] = []
                return Response(success)
            serializer = NotificationSerializer(notifications[int(page) - 30:int(page)], many=True)
            data_lists = []
            for i in serializer.data:
                if i['notifType'] == 1:
                    data = getTypeOneNotificationDetails(i)
                    if data is not None:
                        data_lists.append(data)
                elif i['notifType'] == 2:
                    data = getTypeTwoNotificationDetails(i)
                    if data is not None:
                        data_lists.append(data)
                elif i['notifType'] == 3:
                    data = getTypeThreeNotificationDetails(i)
                    if data is not None:
                        data_lists.append(data)
            if len(data_lists) >= 30:
                hasMorePage = True
            else:
                hasMorePage = False

            success['hasMorePage'] = bool(hasMorePage)
            success['message'] = "success"
            success['data'] = data_lists
            return Response(success)
        err_401['message'] = "invalid user"
        return Response(err_401)
class LikeNotificationView:
    def saveLike(ako: AbstractBaseUser, postId: str) -> None:
        name = Profile.objects.get(user=ako).name
        if name == "" or name is None:
            name = ako.username
        try:
            creator_usr = Post.objects.filter(Q(id=postId) | Q(images_url__id=str(postId))).first().creator
        except Post.DoesNotExist:
            return
        creator:AbstractBaseUser = User.objects.get(username=creator_usr)
        if creator.username == ako.username:
            name = "You"
        try:
            notif = MyNotification.objects.get(userToNotify=creator, subjectPostsId=postId, notifType=2)
            if not ako in notif.subjectUser.all():
                notif.subjectUser.add(ako)
            title = f"{name} and {str(len(notif.subjectUser.all()) - 1)} others reacted in your posts" if len(
                notif.subjectUser.all()) > 1 else f"{name} reacted in your posts"
            notif.title = title
            notif.save()
            pushBadge(creator=creator)
            return
        except MyNotification.DoesNotExist:
            notif = MyNotification.objects.create(userToNotify=creator, subjectPostsId=postId, title=f"{name} reacted in your posts",
                                                  description="", notifType=2)
            notif.subjectUser.add(ako)
            notif.save()
            pushBadge(creator=creator)
            return

    def deleteNotification(ako: AbstractBaseUser, postId: str) -> None:
        try:
            creator = User.objects.get(username=Post.objects.get(Q(id=postId) | Q(images_url__id=str(postId))).creator)
        except Exception as e:
            print(e)
            return
        try:
            notif = MyNotification.objects.get(userToNotify=creator, subjectPostsId=postId, description="", notifType=2)
            if ako in notif.subjectUser.all():
                notif.subjectUser.remove(ako)
                if len(notif.subjectUser.all()) == 0:
                    notif.delete()
                else:
                    name = notif.subjectUser.all()[0].username
                    if name == creator.username:
                        name = "You"
                    if len(notif.subjectUser.all()) == 1:
                        notif.title = f"{name} reacted in your posts"
                    else:
                        notif.title = f"{name} and {str(len(notif.subjectUser.all()) - 1)} reacted in your posts"
                    notif.save()
            return
        except MyNotification.DoesNotExist:
            pass

        return


class CommentNotificationView:
    def Notify(post_id: str, request: HttpRequest):
        name = Profile.objects.get(user=request.user).name
        if name == "" or name is None:
            name = request.user.username
        creator:AbstractBaseUser = User.objects.get(
            username=Post.objects.filter(Q(id=post_id) | Q(images_url__id=str(post_id))).first().creator)
        if creator == request.user:
            return

        try:
            notif = MyNotification.objects.get(userToNotify=creator, subjectPostsId=post_id, notifType=3)
            notif.title = f"{name} and {str(len(notif.subjectUser.all()))} others commented on your posts"
            if not request.user in notif.subjectUser.all():
                notif.subjectUser.add(request.user)

            notif.seen = False
            notif.save()
            pushBadge(creator=creator)

        except MyNotification.DoesNotExist:
            notif = MyNotification.objects.create(userToNotify=creator, subjectPostsId=post_id,
                                                  title=f"{name} commented on your posts", description="", notifType=3)
            notif.subjectUser.add(request.user)
            notif.save()
            pushBadge(creator=creator)
        return


class FollowNotificationView:
    def Notify(request: HttpRequest, following: AbstractBaseUser):
        name = Profile.objects.get(user=request.user).name
        if name == "" or name is None or str(name).replace(" ", "") == "":
            name = request.user.username

        if FollowerCount.objects.filter(follower=following, user=request.user).exists():
            if not MyNotification.objects.filter(userToNotify=following, subjectUser__pk=request.user.id,
                                                 title=f"{str(name)} and you are now friends.").first():
                notif = MyNotification.objects.create(userToNotify=following, title=f"{str(name)} and you are now friends.",
                                                      description=str(name) + " followed you", notifType=1,
                                                      subjectPostsId
                                        =request.user.username)
                notif.subjectUser.add(request.user)
                notif.save()
                pushBadge(creator=following)
        else:
            if not MyNotification.objects.filter(userToNotify=following, subjectUser__pk=request.user.id,
                                                 title=f"{str(name)} followed you.").first():
                notif = MyNotification.objects.create(userToNotify=following, title=f"{str(name)} followed you.",
                                                      description=str(name) + " followed you", notifType=1,
                                                      subjectPostsId
                                        =request.user.username)
                notif.subjectUser.add(request.user)
                notif.save()
                pushBadge(creator=following)

    def deleteNotif(request: HttpRequest, following: AbstractBaseUser):
        name = Profile.objects.get(user=request.user).name
        if name == "" or name is None or str(name).replace(" ", "") == "":
            name = request.user.username
        try:
            note = MyNotification.objects.get(userToNotify=following, subjectUser__pk=request.user.id,
                                              title=f"{str(name)} followed you.",
                                              description=str(name) + " followed you")
            note.delete()
        except MyNotification.DoesNotExist:
            pass
        try:
            note = MyNotification.objects.get(userToNotify=following, subjectUser__pk=request.user.id,
                                              title=f"{str(name)} and you are now friends.",
                                              description=str(name) + " followed you")
            note.delete()
        except MyNotification.DoesNotExist:
            pass
        return
