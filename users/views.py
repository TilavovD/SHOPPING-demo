from django.contrib.auth import login
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from .serializers import UserDetailSerializer, LoginSerializer, UserRegisterSerializer, SecretCodeSerializer
from .helpers import send_secret_code
from rest_framework import permissions, status


# Create your views here.

class UserDetailView(RetrieveAPIView):
    queryset = User.objects.filter(is_superuser=True)
    serializer_class = UserDetailSerializer

    def get_queryset(self, **kwargs):
        print(self.kwargs)
        return self.queryset.filter(pk=self.kwargs['pk'])


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(phone_number=request.data['phone_number'], is_verified=False)
        if user:
            user[0].delete()
        response = self.create(request, *args, **kwargs)
        user = User.objects.get(phone_number=request.data['phone_number'])
        secret_key = send_secret_code(request.data['phone_number'])
        user.secret_key = secret_key
        user.save()
        return response


class CheckSecretCodeAPIView(APIView):
    serializer_class = SecretCodeSerializer

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
