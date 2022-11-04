from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


# Create your views here.
class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
