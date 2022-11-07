from django.urls import path

from .views import CartListAPIView

app_name = 'orders'

urlpatterns = [
    path('', CartListAPIView.as_view(), name='list')
]
