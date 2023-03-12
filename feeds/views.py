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
# Create your views here.


class newsfeed(APIView):
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
                feed_lists = Post.objects.filter(creator=usernames).order_by("created_at")
                for x in feed_lists:
                    feed.append(x)
            y = PostSerializer(feed[int(limit)-16:int(limit)], many = True)
            for i in y.data:
                i['creator_avatar'] = getAvatarByUsername(i['creator'])
                i['your_avatar'] = me.data['profileimg']
                i['created_at'] = getStringTime(i['created_at'])
            if len(y.data) == 16:
                return JsonResponse({'status_code': 200, 'status': True, 'message': 'success', 'hasMorePage': True, 'data': y.data})
            else:
                return JsonResponse({'status_code': 200, 'status': True, 'message': 'success', 'hasMorePage': False, 'data': y.data})

        return JsonResponse({'status': False, 'status_code': 401, 'message': 'user not logged'})
