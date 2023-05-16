from users.models import FollowerCount
from posts.models import Post, LikePost
from django.contrib.auth.models import AbstractBaseUser

def getAllRelations(user:AbstractBaseUser) -> list[AbstractBaseUser]:
    user_following_list = [users.user for users in FollowerCount.objects.filter(follower=user)]
    user_following_list.append(user)
    return user_following_list