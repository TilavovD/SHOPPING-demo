from django.urls import path
from rest_framework.authtoken import views

from .views import UserDetailView, UserCreateView, CheckSecretCodeAPIView, LoginView

urlpatterns = [
    path("<int:pk>", UserDetailView.as_view(), name='user_detail'),
    path("create", UserCreateView.as_view(), name='user_create'),
    path('api-token-auth', views.obtain_auth_token),
    path('verify_secret_code', CheckSecretCodeAPIView.as_view(), name="verify_code"),
    path('login', LoginView.as_view(), name="login")

]
