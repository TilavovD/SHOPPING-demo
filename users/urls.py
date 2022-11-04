from django.urls import path
from .views import UserDetailView, UserCreateView

urlpatterns = [
    path("<int:pk>", UserDetailView.as_view(), name='user_detail'),
    path("create", UserCreateView.as_view(), name='user_create'),
]
