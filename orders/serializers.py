from rest_framework import serializers

from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):

    price_without_discount = serializers.SerializerMethodField('price_without_discount_func')
    price_after_discount = serializers.SerializerMethodField('price_after_discount_func')
    amount_saved = serializers.SerializerMethodField('amount_saved_func')
    final_price = serializers.SerializerMethodField('final_price_func')

    def price_without_discount_func(self, object):
        return object.get_total_item_price()

    def price_after_discount_func(self, object):
        return object.get_total_discount_item_price()

    def amount_saved_func(self, object):
        return object.get_amount_saved()

    def final_price_func(self, object):
        return object.get_final_price()

    class Meta:
        model = CartItem
        fields = '__all__'
