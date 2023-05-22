from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework import serializers
from rest_framework import response
from .serializers import CustomTokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings

DEVICE_KEY = "My_device_key"


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def add_to_blackList(base64_encoded_token_string):
    token = RefreshToken(base64_encoded_token_string)
    token.blacklist()

def tfa_verify_code(self, request):
        """Verify given code validity."""
        serializer = serializers.VerifyTFACodeSerializer(
            data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        refresh = RefreshToken.for_user(request.user)
        refresh[DEVICE_KEY] = (
            serializer.validated_data["code"].persistent_id)
        return response.Response({
            "refreshToken": str(refresh),
            "accessToken": str(refresh.access_token)
        })

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

