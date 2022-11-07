from django.db import models

from users.models import User
from products.models import Product


# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(
        User,
        related_name='cart_items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} added to cart by {self.user}"

    def get_total_item_price(self):
        return self.product.price * self.amount

    def get_total_discount_item_price(self):
        return int(self.product.get_price_after_discount() * self.amount)

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.product.discount_percent > 0:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
