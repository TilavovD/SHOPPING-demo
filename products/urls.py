from django.urls import path

from .views import (
    CategoryListAPIView,

    ProductListAPIView,
    ProductDetailAPIView,
    FavouriteProductListAPIView,
    AddFavouriteProductListAPIView,

)


app_name = 'products'

urlpatterns = [
    path('', ProductListAPIView.as_view(), name='list'),
    path('<int:pk>/', ProductDetailAPIView.as_view(), name='detail'),

    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('wishlist/', FavouriteProductListAPIView.as_view(), name='wishlist'),
    path('wishlist/add/', AddFavouriteProductListAPIView.as_view(), name='wishlist-add'),

]
