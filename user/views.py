from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from jwt import InvalidTokenError
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework.response import Response

from HerbalPureAPI import settings
from user.serializers import UserSerializer, CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer, \
    ContactUsSerializer


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


class ContactUsView(generics.CreateAPIView):
    serializer_class = ContactUsSerializer
    permission_classes = []
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data["name"]
            email = serializer.validated_data["email"]
            message = serializer.validated_data["message"]

            send_mail(
                f"Message from {name} ({email})",
                message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
            )

            return Response(
                {"message": "Message sent successfully!"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
