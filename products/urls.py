from django.urls import path

from .views import (
    MainCategoryListAPIView,

    ProductListAPIView,
    ProductDetailAPIView,
    FavouriteProductListAPIView,
    AddFavouriteProductAPIView,
    DeleteFavouriteProductAPIView,

)


app_name = 'products'

urlpatterns = [
    path('', ProductListAPIView.as_view(), name='list'),
    path('<int:pk>/', ProductDetailAPIView.as_view(), name='detail'),

    path('categories/', MainCategoryListAPIView.as_view(), name='category-list'),
    path('wishlist/', FavouriteProductListAPIView.as_view(), name='wishlist'),
    path('wishlist/add/', AddFavouriteProductAPIView.as_view(), name='wishlist-add'),
    path('wishlist/<int:pk>/delete/', DeleteFavouriteProductAPIView.as_view(), name='wishlist-item-delte'),

]
