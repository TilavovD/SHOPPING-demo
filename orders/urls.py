from django.urls import path

from .views import CartListAPIView, CartItemAPIView, AddressListAPIView

app_name = 'orders'

urlpatterns = [
    path('cart/', CartListAPIView.as_view(), name='cart-list'),
    path('cart/<int:pk>/', CartItemAPIView.as_view(), name='cart-item'),
    path('addressess/', AddressListAPIView.as_view(), name='address-list'),

]
