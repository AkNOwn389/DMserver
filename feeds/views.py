from django.shortcuts import render
from profiles.serializers import ProfileSerializer
from profiles.models import Profile
from users.models import FollowerCount
from posts.models import Post
from posts.serializers import PostSerializer
from time_.get_time import getStringTime
from rest_framework.views import APIView
from profiles.views import getAvatarByUsername
from django.http import JsonResponse
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
                feed_lists = Post.objects.filter(creator=usernames).order_by("-created_at")
                for x in feed_lists:
                    feed.append(x)
            y = PostSerializer(feed[int(limit)-16:int(limit)], many = True)
            for i in y.data:
                
                i['creator_avatar'] = getAvatarByUsername(i['creator'])
                i['your_avatar'] = me.data['profileimg']
                i['dateCreated'] = i['created_at']
                i['created_at'] = getStringTime(i['created_at'])
            if len(y.data) == 16:
                self.data['hasMorePage'] = True
                self.data['data'] = y.data
                return JsonResponse(self.data)
            else:
                self.data['hasMorePage'] = False
                self.data['data'] = y.data
                return JsonResponse(self.data)

        return JsonResponse(self.err)
    

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

