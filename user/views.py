from django.contrib.auth import get_user_model
from jwt import InvalidTokenError
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework.response import Response

from user.serializers import UserSerializer, CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        email = request.data.get("email")
        user = get_user_model().objects.get(email=email)
        user_info_serializer = UserSerializer(user)
        user_info_data = user_info_serializer.data
        data = {
            "access": response.data["access"],
            "refresh": response.data["refresh"],
            "user": user_info_data
        }
        return Response(data)


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        try:
            user = JWTAuthentication().get_user(AccessToken(response.data["access"]))
            user_info_serializer = UserSerializer(user)
            user_info_data = user_info_serializer.data
            data = {
                "access": response.data["access"],
                "refresh": response.data["refresh"],
                "user": user_info_data
            }
            return Response(data)
        except (InvalidTokenError, TokenError):
            return Response(status=status.HTTP_401_UNAUTHORIZED)