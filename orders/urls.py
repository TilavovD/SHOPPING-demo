from django.urls import path

from .views import (
    CartListAPIView,
    AddCartItemAPIView,
    CartItemAPIView,

    AddressCreateAPIView,
    AddressDetailAPIView,

    CreateOrderAPIVIew,
    OrderHistoryListAPIVIew,
    OrderDetailAPIView,

    StripeConfigView,
    StripeSessionView,
    PaymentSuccessAPIView,
    PaymentCancelAPIView,
    stripe_webhook_view,
)

app_name = 'orders'

urlpatterns = [
    path('cart/', CartListAPIView.as_view(), name='cart-list'),
    path('cart/add/', AddCartItemAPIView.as_view(), name='cart-add'),
    path('cart/<int:pk>/', CartItemAPIView.as_view(), name='cart-item'),
    path('address/create', AddressCreateAPIView.as_view(), name='address-create'),
    path('address/detail/', AddressDetailAPIView.as_view(), name='address-detail'),

    path('create-order/', CreateOrderAPIVIew.as_view(), name='create-order'),
    path('order-history/', OrderHistoryListAPIVIew.as_view(), name='order-history'),
    path('order-history/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),

    path('payment/stripe-config', StripeConfigView.as_view(), name='stripe-config'),
    path('payment/', StripeSessionView.as_view(), name='stripe-session'),
    path('payment/success/', PaymentSuccessAPIView.as_view(), name='payment-success'),
    path('payment/cancel/', PaymentCancelAPIView.as_view(), name='payment-cancel'),
    path('webhook/', stripe_webhook_view, name='webhook'),

]
