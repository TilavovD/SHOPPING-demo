from rest_framework.generics import ListAPIView, RetrieveAPIView

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


# Create your views here.
class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'price': ['gt', 'lt'],
        'category': ['exact']
    }
    search_fields = ['name']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        queryset = Product.objects.all()

        in_discount = self.request.query_params.get('in_discount', '')
        if in_discount == 'true':
            return queryset.filter(discount_percent__gt=0)
        elif in_discount == 'false':
            return queryset.filter(discount_percent=0)
        else:
            return queryset


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
