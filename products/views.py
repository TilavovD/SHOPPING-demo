from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Product, FavouriteProduct
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    FavouriteProductSerializer,
    AddFavouriteProductSerializer,
)


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
            queryset = queryset.filter(discount_percent__gt=0)
        elif in_discount == 'false':
            queryset = queryset.filter(discount_percent=0)

        # category_name = self.request.query_params.get('category', None)
        # while category_name:
        #     temp_quaryset = queryset.filter(category=category_name)
        #     if temp_quaryset.count() > 0:
        #         return temp_quaryset
        #     category_name =
        return queryset


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class FavouriteProductListAPIView(ListAPIView):
    serializer_class = FavouriteProductSerializer

    def get_queryset(self):
        user = self.request.user
        return FavouriteProduct.objects.filter(user=user)


class AddFavouriteProductListAPIView(CreateAPIView):
    serializer_class = AddFavouriteProductSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class DeleteFavouriteProductListAPIView(DestroyAPIView):
#     serializer_class = AddFavouriteProductSerializer
#
#     def perform_destroy(self, instance):

