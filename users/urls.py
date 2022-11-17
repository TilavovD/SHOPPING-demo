from django.urls import path
from rest_framework.authtoken import views

from .views import UserDetailView, UserCreateView, CheckSecretCodeAPIView, LoginView, LogOutView

app_name = 'users'

urlpatterns = [
    path("detail/", UserDetailView.as_view(), name='user_detail'),
    path("create/", UserCreateView.as_view(), name='user_create'),
    path('api-token-auth/', views.obtain_auth_token),
    path('verify_secret_code/', CheckSecretCodeAPIView.as_view(), name="verify_code"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogOutView.as_view(), name="logout"),

]
