from django.urls import path
from rest_framework.authtoken import views

from .views import UserDetailView, UserCreateView

urlpatterns = [
    path("<int:pk>", UserDetailView.as_view(), name='user_detail'),
    path("create", UserCreateView.as_view(), name='user_create'),
    path('api-token-auth', views.obtain_auth_token),
]
