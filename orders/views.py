from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from django.db import models

from .models import CartItem
from .serializers import CartItemSerializer


# Create your views here.
class CartListAPIView(ListAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = CartItemSerializer(queryset, many=True)

        result_data = {
            'final_price': 100,
            'total_amount_saved': 100,
            'items_data': serializer.data
        }

        return Response(result_data)
