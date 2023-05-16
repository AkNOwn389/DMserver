from django.shortcuts import render
from profiles.serializers import ProfileSerializer
from profiles.models import Profile
from users.models import FollowerCount
from posts.models import Post, LikePost
from posts.serializers import PostSerializer, LikesPostSerializer
from time_.get_time import getStringTime
from rest_framework.response import Response
from rest_framework.views import APIView
from profiles.views import getAvatarByUsername
from django.http import JsonResponse, HttpRequest
from django.db.models import Q
from .dbManager import getAllRelations
from django.contrib.auth.models import AbstractBaseUser

# Create your views here.


class newsfeed(APIView):
    err = {'status': False, 'status_code': 401, 'message': 'user not logged'}
    data = {'status_code': 200, 'status': True, 'message': 'success'}

    def get(self, request:HttpRequest, page:int):
        if request.user.is_authenticated:
            me = Profile.objects.filter(user = request.user).first()
            me = ProfileSerializer(me)
            limit = page*16
            user_following_list = getAllRelations(request.user)
            feed_lists = Post.objects.none()
            for usernames in user_following_list:
                if usernames == request.user:
                    feed_lists |= Post.objects.filter(Q(creator=usernames, privacy= "F") | Q(creator=usernames, privacy= "P") | Q(creator=usernames, privacy= "O"))
                elif FollowerCount.objects.filter(user = usernames, follower = request.user).exists():
                    feed_lists |= Post.objects.filter(Q(creator=usernames, privacy= "F") | Q(creator=usernames, privacy= "P"))
                else:
                    feed_lists |= Post.objects.filter(creator=usernames, privacy= "P")
            feed_lists = feed_lists.order_by("-created_at")
            
            y = PostSerializer(feed_lists[int(limit)-16:int(limit)], many = True)
            for i in y.data:
                if len(i['image_url']) == 0 and len(i['videos_url']) == 1:
                    i['media_type'] = 6
                    i['videos'] = i['videos_url'][0]['url_w500']
                    i['url_w1000'] = i['videos_url'][0]['url_w1000']
                    i['url_w250'] = i['videos_url'][0]['url_w250']
                    i['playback_url'] = i['videos_url'][0]['playback_url']
                    i['thumbnail'] = i['videos_url'][0]['thumbnail']
                    i['width'] = i['videos_url'][0]['width']
                    i['height'] = i['videos_url'][0]['height']
                    del i['image_url']
                    del i['videos_url']

                i['creator_avatar'] = getAvatarByUsername(i['creator'])
                i['your_avatar'] = me.data['profileimg']
                i['dateCreated'] = i['created_at']
                i['created_at'] = getStringTime(i['created_at'])
                i['me'] = True if i['creator'] == request.user.username else False
                if LikePost.objects.filter(post_id=i['id'], username=request.user).exists():
                    i['is_like'] = True
                    i['reactionType'] = LikesPostSerializer(LikePost.objects.filter(post_id=i['id'], username=request.user).first()).data['reactionType']
                else:
                    i['is_like'] = False
            if len(y.data) == 16:
                self.data['nextPageKey'] = page+1
                self.data['hasMorePage'] = True
                self.data['data'] = y.data
                return JsonResponse(self.data)
            else:
                self.data['hasMorePage'] = False
                self.data['nextPageKey'] = 1
                self.data['data'] = y.data
                return JsonResponse(self.data)

        return JsonResponse(self.err)
class VideosFeed(APIView):
    err = {'status': False, 'status_code': 401, 'message': 'user not logged'}
    def get(self, request:HttpRequest, page):
        if request.user.is_authenticated:
            user:AbstractBaseUser = request.user
            me = Profile.objects.filter(user = user).first()
            me = ProfileSerializer(me)
            limit = page*16
            all_creators = getAllRelations(user=user)
            
            video_feed = Post.objects.none()
            for creator in all_creators:
                creator:AbstractBaseUser = creator
                if creator.username == request.user.username:
                    video_feed |= Post.objects.filter(creator=user.pk, media_type = 5)
                elif FollowerCount.objects.filter(user = creator.pk, follower = request.user).exists():
                    video_feed |= Post.objects.filter(Q(creator = creator.pk, privacy ="F", media_type = 5) | Q(creator = creator.pk, privacy ="P", media_type = 5))
                else:
                    video_feed |=  Post.objects.filter(creator = creator.pk, privacy = "P", media_type = 5)
                    
            DATA = PostSerializer(video_feed[int(limit)-16:int(page)*16], many = True).data
            
            """
            try:
                    post = Post.objects.filter(creator = user, media_type = 5).order_by("-created_at")
                    video_feed.extend(PostSerializer(post, many = True).data)
                except Exception as e:
                    pass

                if FollowerCount.objects.filter(user = creator.user, follower = user).first():
                    user_all_posts = Post.objects.filter(Q(creator = creator.user, privacy ="F", media_type = 5) | Q(creator = creator.user, privacy ="P", media_type = 5))
                    if not user_all_posts is None:
                        video_feed.extend(PostSerializer(user_all_posts, many = True).data)
                else:
                    user_all_posts = Post.objects.filter(creator = creator, privacy = "P", media_type = 5)
                    if not user_all_posts is None:
                        video_feed.extend(PostSerializer(user_all_posts, many = True).data)
            """
            
            
            
            if len(DATA) < 16:
                a = 0
                while True:
                    dagdag = Post.objects.filter(privacy = "P", media_type = 5).order_by("created_at")
                    try:
                        b = PostSerializer(dagdag[a]).data
                    except IndexError:
                        break
                    if not b in DATA or not b in video_feed:
                        DATA.append(b)
                    else:
                        a+=1
                    if len(DATA) == 16:
                        break
            
            for i in DATA:
                if len(i['videos_url']) == 0:
                    DATA.remove(i)
                    continue
                i['media_type'] = 6 if i['media_type'] == 5 else 5
                i['creator_avatar'] = getAvatarByUsername(i['creator'])
                i['your_avatar'] = me.data['profileimg']
                i['dateCreated'] = i['created_at']
                i['created_at'] = getStringTime(i['created_at'])
                i['me'] = True if i['creator'] == request.user.username else False
                if LikePost.objects.filter(post_id=i['id'], username=request.user).exists():
                    i['is_like'] = True
                    i['reactionType'] = LikesPostSerializer(LikePost.objects.filter(post_id=i['id'], username=request.user).first()).data['reactionType']
                else:
                    i['is_like'] = False
                try:
                    i['video_url'] = i['videos_url'][0]['url_w1000']
                    i['thumbnail'] = i['videos_url'][0]['thumbnail']
                    i['width'] = i['videos_url'][0]['width']
                    i['height'] = i['videos_url'][0]['height']
                    i['url_w500'] = i['videos_url'][0]['url_w500']
                    i['url_w250'] = i['videos_url'][0]['url_w250']
                    i['playback_url'] = i['videos_url'][0]['playback_url']
                except Exception as e:
                    DATA.remove(i)
            #FILTER 1
            for i in DATA:
                try:
                    del i['videos_url']
                except:
                    pass
                try:
                    del i['image_url']
                except:
                    pass
            #FILTER 2 remove none video
            for i in DATA:
                try:
                    i['video_url']
                except KeyError:
                    DATA.remove(i)
            #FILTER 3
            for i in DATA:
                try:
                    i['image_url']
                    del i['image_url']
                except KeyError:
                    pass
                try:
                    i['videos_url']
                    del i['videos_url']
                except KeyError:
                    pass
            return Response({
                'status':True,
                'status_code': 200,
                'message': 'success',
                'hasMorePage': True if len(DATA) == 16 else False,
                'len': len(DATA),
                'data': DATA
            })
        return Response(self.err)
            


class MyPostView(APIView):
    err = {"status": False, "status_code": 401, "message": "invalidated"}
    err_not_foud = {"status": False, "status_code": 404, "message": "Not found"}
    no_data = {"status": False, "status_code": 200, "message": "no posts", "data": []}
    data = {"status": True, "status_code": 200, "message": "success"}

    def get(self, request, page):
        if request.user.is_authenticated:
            user = request.user
            page = page*16
            post = Post.objects.filter(creator = user)
            if post is None:
                return JsonResponse(self.no_data)
            serializer = PostSerializer(post[int(page)-16: int(page)], many=True)
            self.data['data'] = serializer.data
            return JsonResponse(data=self.data)
        return JsonResponse(self.err)

class NewsView(APIView):
    def get(self, request:HttpRequest):
        if request.user.is_authenticated:
            pass