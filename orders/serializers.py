from rest_framework import serializers

from .models import CartItem, Address
from products.serializers import ProductSerializer


class CartItemListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    price_without_discount = serializers.SerializerMethodField('price_without_discount_func')
    price_after_discount = serializers.SerializerMethodField('price_after_discount_func')
    amount_saved = serializers.SerializerMethodField('amount_saved_func')
    final_price = serializers.SerializerMethodField('final_price_func')

    def price_without_discount_func(self, obj):
        return obj.get_total_item_price()

    def price_after_discount_func(self, obj):
        return obj.get_total_discount_item_price()

    def amount_saved_func(self, obj):
        return obj.get_amount_saved()

    def final_price_func(self, obj):
        return obj.get_final_price()

    class Meta:
        model = CartItem
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ('user', )


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'
