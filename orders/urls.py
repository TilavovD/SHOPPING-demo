from django.urls import path

from .views import (
    CartListAPIView,
    CartItemAPIView,
    AddressListAPIView,
    StripeConfigView,
    StripeSessionView,

)

app_name = 'orders'

urlpatterns = [
    path('cart/', CartListAPIView.as_view(), name='cart-list'),
    path('cart/<int:pk>/', CartItemAPIView.as_view(), name='cart-item'),
    path('addressess/', AddressListAPIView.as_view(), name='address-list'),

    path('payment/', StripeSessionView.as_view(), name='stripe-session'),
    path('payment/stripe-config', StripeConfigView.as_view(), name='stripe-config'),

]
