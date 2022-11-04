from django.urls import path

from .views import (
    CategoryListAPIView,

    ProductListAPIView,
    ProductDetailAPIView,
)


app_name = 'product'

urlpatterns = [
    path('', ProductListAPIView.as_view(), name='list'),
    path('<int:pk>/', ProductDetailAPIView.as_view(), name='detail'),

]
