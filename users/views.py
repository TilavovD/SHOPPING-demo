# from rest_framework.generics import RetrieveAPIView, CreateAPIView
# from users.models import User
# from .serializers import UserDetailSerializer
#
#
# # Create your views here.
#
# class UserDetailView(RetrieveAPIView):
#     queryset = User.objects.filter(is_superuser=True)
#     serializer_class = UserDetailSerializer
#
#     def get_queryset(self, **kwargs):
#         print(self.kwargs)
#         return self.queryset.filter(pk=self.kwargs['pk'])
#
# class UserCreateView(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserDetailSerializer
