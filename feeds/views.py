from django.shortcuts import render
from profiles.serializers import ProfileSerializer
from profiles.models import Profile
from users.models import FollowerCount
from posts.models import Post, LikePost
from posts.serializers import PostSerializer
from time_.get_time import getStringTime
from rest_framework.response import Response
from rest_framework.views import APIView
from profiles.views import getAvatarByUsername
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime
# Create your views here.


class newsfeed(APIView):
    err = {'status': False, 'status_code': 401, 'message': 'user not logged'}
    data = {'status_code': 200, 'status': True, 'message': 'success'}

    def get(self, request, page):
        if request.user.is_authenticated:
            me = Profile.objects.filter(user = request.user).first()
            me = ProfileSerializer(me)
            limit = page*16
            user_following_list = []
            feed = []
            
            user_following = FollowerCount.objects.filter(follower=request.user)
            for users in user_following:
                user_following_list.append(users.user)
            user_following_list.append(request.user)
            for usernames in user_following_list:
                if usernames == request.user:
                    feed_lists = Post.objects.filter(Q(creator=usernames, privacy= "F") | Q(creator=usernames, privacy= "P") | Q(creator=usernames, privacy= "O")).order_by("-created_at")
                elif FollowerCount.objects.filter(user = usernames, follower = request.user).first():
                    feed_lists = Post.objects.filter(Q(creator=usernames, privacy= "F") | Q(creator=usernames, privacy= "P")).order_by("-created_at")
                else:
                    feed_lists = Post.objects.filter(creator=usernames, privacy= "P").order_by("-created_at")
                for x in feed_lists:
                    feed.append(x)
            y = PostSerializer(feed[int(limit)-16:int(limit)], many = True)
            for i in y.data:
                if len(i['image_url']) == 0 and len(i['videos_url']) == 1:
                    i['media_type'] = 6
                    i['videos'] = i['videos_url'][0]['url_w500']
                    i['url_w1000'] = i['videos_url'][0]['url_w1000']
                    i['url_w250'] = i['videos_url'][0]['url_w250']
                    i['playback_url'] = i['videos_url'][0]['playback_url']
                    del i['image_url']
                    del i['videos_url']
                i['creator_avatar'] = getAvatarByUsername(i['creator'])
                i['your_avatar'] = me.data['profileimg']
                i['dateCreated'] = i['created_at']
                i['created_at'] = getStringTime(i['created_at'])
                i['me'] = True if i['creator'] == request.user.username else False
                if LikePost.objects.filter(post_id=i['id'], username=request.user).first():
                    i['is_like'] = True
                else:
                    i['is_like'] = False
            if len(y.data) == 16:
                self.data['hasMorePage'] = True
                self.data['data'] = y.data
                return JsonResponse(self.data)
            else:
                self.data['hasMorePage'] = False
                self.data['data'] = y.data
                return JsonResponse(self.data)

        return JsonResponse(self.err)
class VideosFeed(APIView):
    err = {'status': False, 'status_code': 401, 'message': 'user not logged'}
    def get(self, request, page):
        if request.user.is_authenticated:
            user = request.user
            me = Profile.objects.filter(user = user).first()
            me = ProfileSerializer(me)
            limit = page*16
            all_creators = FollowerCount.objects.filter(follower = user)
            video_feed = []
            for creator in all_creators:
                try:
                    post = Post.objects.filter(creator = user, media_type = 5).order_by("-created_at")
                    video_feed.extend(PostSerializer(post, many = True).data)
                except Exception as e:
                    pass

                if FollowerCount.objects.filter(user = creator.user, follower = user).first():
                    user_all_posts = Post.objects.filter(Q(creator = creator.user, privacy = "F", media_type = 5) | Q(creator = creator.user, privacy = "P", media_type = 5))
                    if not user_all_posts is None:
                        video_feed.extend(PostSerializer(user_all_posts, many = True).data)
                else:
                    user_all_posts = Post.objects.filter(creator = creator, privacy = "P", media_type = 5)
                    if not user_all_posts is None:
                        video_feed.extend(PostSerializer(user_all_posts, many = True).data)
            DATA = video_feed[int(limit)-16:int(page)*16]
            if len(DATA) < 16:
                num = 16 -len(DATA)
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
                print(i)
                i['media_type'] = 6 if i['media_type'] == 5 else 5
                i['creator_avatar'] = getAvatarByUsername(i['creator'])
                i['your_avatar'] = me.data['profileimg']
                i['dateCreated'] = i['created_at']
                i['created_at'] = getStringTime(i['created_at'])
                i['me'] = True if i['creator'] == request.user.username else False
                i['is_like'] = True if LikePost.objects.filter(post_id=i['id'], username=request.user).first() else False
                try:
                    i['video_url'] = i['videos_url'][0]['videos']
                    i['thumbnail'] = i['videos_url'][0]['thumbnail']
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

