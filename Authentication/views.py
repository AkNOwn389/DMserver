from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework import serializers
from rest_framework import response
from .. import constants


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
        refresh[constants.TFA_DEVICE_TOKEN_KEY] = (
            serializer.validated_data["code"].persistent_id)
        return response.Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })

"""
def verify(self, request, uid, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(email__iexact=payload['email'])
            email = force_text(urlsafe_base64_decode(uid))
            if user is not None and email == payload['email']:
                if not user.is_email_verified:
                    user.is_active = True
                    user.is_email_verified = True
                    user.save()
                refresh_token = RefreshToken.for_user(user)
                return Response(
                    {
                        'authentication': {
                            'access_token': str(refresh_token.access_token),
                            'refresh_token': str(refresh_token)
                        },
                        'user': UserSerializer(user).data,
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response({'message': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response({'message': 'Token is expired', 'email': email}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'message': 'Token is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError):
            return Response({'message': 'An error occurred, please retry'}, status=status.HTTP_400_BAD_REQUEST)
"""