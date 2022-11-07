from django.urls import path

from .views import CartListAPIView

app_name = 'orders'

urlpatterns = [
    path('cart/', CartListAPIView.as_view(), name='cart-list'),
]
