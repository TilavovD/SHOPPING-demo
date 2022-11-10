from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from .serializers import UserDetailSerializer
import vonage


# Create your views here.

class UserDetailView(RetrieveAPIView):
    queryset = User.objects.filter(is_superuser=True)
    serializer_class = UserDetailSerializer

    def get_queryset(self, **kwargs):
        print(self.kwargs)
        return self.queryset.filter(pk=self.kwargs['pk'])


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        user = User.objects.get(phone_number=request.data['phone_number'])
        print(request.user)
        user.secret_key = 11111
        user.save()
        return response


class CheckSecretCodeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(phone_number=request.data['phone_number'])
            if request.data["secret_key"] == user.secret_key:
                return Response({
                    "status": 200,
                    "message": "User successfully created",
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
