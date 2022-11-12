import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework import permissions

from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
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

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
# CART ITEM VIEWS
# Add some amount of some product to cart by particular user
class AddCartItemAPIView(CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = AddCartItemSerializer

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# List of Products that particular user added his cart to buy
class CartListAPIView(ListAPIView):
    serializer_class = CartItemListSerializer

    permission_classes = [permissions.IsAuthenticated]

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

    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise ValidationError({
                'error': 'You cannot other people\'s cart',
            })
        serializer.save(user=self.request.user)


#  ADDRESS VIEWS
# Add address of particular user and List of all users' address
class AddressListAPIView(CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        queryset = Address.objects.filter(user=self.request.user)
        if queryset.exists():
            raise ValidationError({
                'error': 'You have already added address. You can edit it, but not create new one',
            })
        serializer.save(user=self.request.user)


# Detail, update, delete Adress of particular user
class AddressDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return Address.objects.get(user=user)

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise ValidationError({
                'error': 'You can not delete other people\'s address information',
            })
        instance.delete()


# ORDER VIEWS
# Create order by particular user
class CreateOrderAPIVIew(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def post(self, request, *args, **kwargs):
        user = request.user
        incomplete_orders = Order.objects.filter(user=user, is_paid=False)

        if incomplete_orders.exists():
            order = incomplete_orders[0]
            serializer = OrderSerializer(instance=order, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return self.create(request, *args, **kwargs)


# List Orders History of particular user
class OrderHistoryListAPIVIew(ListAPIView):
    serializer_class = OrderSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)


class StripeConfigView(APIView):
    """
    StripeConfigView is the API of configs resource, and
    responsible to handle the requests of /config/ endpoint.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        config = {
            "publishable_key": settings.STRIPE_PUBLISHABLE_KEY
        }
        return Response(config)


class StripeSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            orders = Order.objects.filter(user=user, is_paid=False)

            if orders.exists():
                order = orders[0]
                unit_amount = order.total_money
            else:
                return Response(
                    {'error': 'You do not have any order yet.'},
                    status=400
                )

            pay_data = {
                'price_data': {
                    "currency": "usd",
                    "unit_amount": unit_amount * 100,
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
                ],
                metadata={
                    'order_id': order.id,
                }
            )

            return redirect(checkout_session.url)
            # return Response(
            #     {
            #         'sessionId': checkout_session['id'],
            #         'session_url': checkout_session['url']
            #      }
            # )
        except Exception as e:
            return Response(
                {
                    'msg': 'something went wrong while creating stripe session',
                    'error': str(e),
                },
                status=500
            )


@csrf_exempt
def stripe_webhook_view(request):

    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_KEY
    event = None

    try:
        event = stripe.Webhook.construct_event(
            request.body, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session['metadata']['order_id']

        orders = Order.objects.filter(id=order_id)
        if orders.exists():
            order = orders[0]
            order.is_paid = True
            order.save()
        else:
            return Response(
                {'error': 'No order found with this order id'},
                status=400
            )

    # Passed signature verification
    return HttpResponse(status=200)
