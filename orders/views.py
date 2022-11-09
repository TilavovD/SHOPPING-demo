import stripe
from django.conf import settings
from rest_framework.exceptions import ValidationError

from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    CreateAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import CartItem, Address, Order
from .serializers import (
    AddCartItemSerializer,
    CartItemListSerializer,
    CartItemSerializer,
    OrderSerializer,
    AddressSerializer,
)


# Create your views here.
# CART ITEM VIEWS
# Add some amount of some product to cart by particular user
class AddCartItemAPIView(CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = AddCartItemSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# List of Products that particular user added his cart to buy
class CartListAPIView(ListAPIView):
    serializer_class = CartItemListSerializer

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user, order__isnull=True)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CartItemListSerializer(queryset, many=True)

        final_price = 0
        total_amount_saved = 0
        for cart_item in serializer.data:
            final_price += cart_item['price_after_discount']
            total_amount_saved += cart_item['amount_saved']

        result_data = {
            'final_price': final_price,
            'total_amount_saved': total_amount_saved,
            'items_data': serializer.data
        }

        return Response(result_data)


# Detail, update, delete some cart item of particular user
class CartItemAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


#  ADDRESS VIEWS
# Add address of particular user and List of all users' address
class AddressListAPIView(ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        queryset = Address.objects.filter(user=self.request.user)
        if queryset.exists():
            raise ValidationError('You have already added address. You can edit it, but not create new one')
        serializer.save(user=self.request.user)


# Detail, update, delete Adress of particular user
class AddressDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer

    def get_object(self):
        user = self.request.user
        return Address.objects.get(user=user)

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise ValidationError('You can not delete other people\'s address information')
        instance.delete()


# ORDER VIEWS
# Create order by particular user
class CreateOrderAPIVIew(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


# List Orders History of particular user
class OrderHistoryListAPIVIew(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = OrderSerializer(queryset, many=True)
    #
    #     result_data = serializer.data
    #
    #     for  in result_data:
    #
    #
    #     result_data = {
    #         'final_price': final_price,
    #         'total_amount_saved': total_amount_saved,
    #         'items_data': serializer.data
    #     }


class StripeConfigView(APIView):
    """
    StripeConfigView is the API of configs resource, and
    responsible to handle the requests of /config/ endpoint.
    """
    def get(self, request):
        config = {
            "publishable_key": settings.STRIPE_PUBLISHABLE_KEY
        }
        return Response(config)


class StripeSessionView(APIView):
    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        pay_data = {
            'price_data': {
                "currency": "usd",
                "unit_amount": 1000,
                "product_data": {
                    "name": "product_name",
                    "images": [],
                }
            },
            "quantity": 1,
        }

        checkout_session = stripe.checkout.Session.create(
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
            mode='payment',
            line_items=[
                pay_data,
            ]
        )

        return Response(
            {
                'sessionId': checkout_session['id'],
                'session_url': checkout_session['url']
             }
        )
