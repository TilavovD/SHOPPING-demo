from rest_framework import serializers

from .models import Category, Product, FavouriteProduct


class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name",)


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        depth = 1


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
