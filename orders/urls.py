from django.urls import path

from .views import (
    CartListAPIView,
    AddCartItemAPIView,
    CartItemAPIView,

    AddressListAPIView,
    AddressDetailAPIView,

    StripeConfigView,
    StripeSessionView,

    CreateOrderAPIVIew,
    OrderHistoryListAPIVIew,

)

app_name = 'orders'

urlpatterns = [
    path('cart/', CartListAPIView.as_view(), name='cart-list'),
    path('cart/add/', AddCartItemAPIView.as_view(), name='cart-add'),
    path('cart/<int:pk>/', CartItemAPIView.as_view(), name='cart-item'),
    path('addressess/', AddressListAPIView.as_view(), name='address-list'),
    path('address/detail/', AddressDetailAPIView.as_view(), name='address-detail'),

    path('payment/', StripeSessionView.as_view(), name='stripe-session'),
    path('payment/stripe-config', StripeConfigView.as_view(), name='stripe-config'),

    path('create-order/', CreateOrderAPIVIew.as_view(), name='create-order'),
    path('order-history/', OrderHistoryListAPIVIew.as_view(), name='order-history'),

]
