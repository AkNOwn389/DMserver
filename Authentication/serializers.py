from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from django.contrib.auth.models import AbstractBaseUser
from .models import UserRegisterCode, UserRecoveryCode, RecoveryAccountSpecialId
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from rest_framework_simplejwt.serializers import TokenRefreshSerializer

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(CustomTokenRefreshSerializer, self).validate(attrs)
        # change key names here
        data['accesstoken'] = data.pop('access')
        data['refresh_token'] = data.pop('refresh')
        return data


class UserRegisterCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRegisterCode
        fields = ['id', 'email', 'code', 'expiration', 'date', 'attempt']
        
class UserRecoveryCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRecoveryCode
        fields = ['id', 'email', 'verificationCode', 'expiration', 'date', 'attempt']

class RecoverAccountSpecialIdSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RecoveryAccountSpecialId
        fields = ['id', 'accountToRecover', 'email', 'date', 'attempt']
        
        

class TokenObtainPairResponseSerializer(serializers.Serializer):
    accessToken = serializers.CharField()
    refreshToken = serializers.CharField()
    
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshResponseSerializer(serializers.Serializer):
    accessToken = serializers.CharField()
    refreshToken = serializers.CharField()
    
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenBlacklistResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenBlacklistView(TokenBlacklistView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenBlacklistResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user:AbstractBaseUser):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['username'] = user.username
        # ...

        return token
    

    
"""
check_password(raw_password: str) → None
delete() → None
get_all_permissions(obj: Optional[object] = None) → set
get_group_permissions(obj: Optional[object] = None) → set
get_username() → str
groups
has_module_perms(module: str) → bool
has_perm(perm: str, obj: Optional[object] = None) → bool
has_perms(perm_list: List[str], obj: Optional[object] = None) → bool
id
is_active= True
is_anonymous
is_authenticated
is_staff
is_superuser
pk
save() → None
set_password(raw_password: str) → None
user_permissions
username
"""

"""
def validate(self, attrs):
    data = super().validate(attrs)
    refresh = self.get_token(self.user)
    data["refresh"] = str(refresh)   # comment out if you don't want this
    data["access"] = str(refresh.access_token)
    data["email"] = self.user.email

    Add extra responses here should you wish
    data["userid"] = self.user.id
    data["my_favourite_bird"] = "Jack Snipe"
    
    return data
"""