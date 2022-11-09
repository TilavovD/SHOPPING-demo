from rest_framework import serializers

from .models import CartItem, Address, Order
from products.serializers import ProductSerializer


# Add some amount of some product to cart by particular user
class AddCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ('user', )


# List of Products that particular user added his cart to buy
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


# Detail, update, delete some cart item of particular user
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ('user', )


# Add, detail, update, delete address of particular user
class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('user', )


class OrderSerializer(serializers.ModelSerializer):

    items = serializers.SerializerMethodField('items_func', read_only=True)

    def items_func(self, obj):
        queryset = CartItem.objects.filter(order=obj)
        ser = CartItemSerializer(queryset, many=True)
        return ser.data

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('user', 'is_paid', )
