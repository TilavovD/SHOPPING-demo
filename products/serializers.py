from rest_framework import serializers

from .models import Category, Product, FavouriteProduct


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class FavouriteProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = FavouriteProduct
        fields = '__all__'


class AddFavouriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteProduct
        fields = '__all__'
