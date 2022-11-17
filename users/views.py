from django.contrib.auth import login, logout
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from .serializers import UserDetailSerializer, LoginSerializer, UserRegisterSerializer, SecretCodeSerializer
from .helpers import send_secret_code_via_eskiz
from rest_framework import permissions


# Create your views here.

class UserDetailView(RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        return self.request.user


class UserCreateView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(phone_number=request.data['phone_number'], is_verified=False)
        if user:
            user[0].delete()
        response = self.create(request, *args, **kwargs)
        user = User.objects.get(phone_number=request.data['phone_number'])
        secret_key = send_secret_code_via_eskiz(request.data['phone_number'])
        user.secret_key = secret_key
        user.save()
        return response


class CheckSecretCodeAPIView(APIView):
    serializer_class = SecretCodeSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(phone_number=request.data['phone_number'])
            if request.data["secret_key"] == user.secret_key:
                user.is_verified = True
                user.save()
                return Response({
                    "status": 200,
                    "message": "Phone number successfully verified",
                })
            else:
                return Response({
                    "status": 401,
                    "message": "Provided wrong secret key",
                })
        except User.DoesNotExist as e:
            return Response({
                "status": 401,
                "message": "Wrong credentials",
            })


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        return Response({
            "status": 200,
            "message": "User successfully logged in"
        })


class LogOutView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        request.user.auth_token.delete()
        logout(request)

        return Response('User Logged out successfully')
