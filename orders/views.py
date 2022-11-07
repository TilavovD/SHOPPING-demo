from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from .models import CartItem
from .serializers import CartItemListSerializer, CartItemSerializer


# Create your views here.
class CartListAPIView(ListAPIView):
    serializer_class = CartItemListSerializer

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
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


class CartItemAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
