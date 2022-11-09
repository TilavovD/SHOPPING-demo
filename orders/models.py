from django.db import models

from users.models import User
from products.models import Product


# Create your models here.
DELIVERY_TYPES = (
    ("courier", "courier"),
    ("pickup", "pickup"),
)

PAYMENT_TYPE = (
    ('stripe', 'stripe'),
    ('cash', 'cash'),
)


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
    amount = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(
        'Order',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

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


class Address(models.Model):
    user = models.OneToOneField(
        User,
        related_name='address',
        on_delete=models.CASCADE
    )
    city_address = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user} address"

    class Meta:
        verbose_name_plural = 'Addresses'


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    city_address = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)

    delivery_method = models.CharField(
        max_length=15,
        choices=DELIVERY_TYPES,
        default=DELIVERY_TYPES[0][0]
    )

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    payment_method = models.CharField(
        max_length=15,
        choices=PAYMENT_TYPE,
        default=PAYMENT_TYPE[1][0]
    )

    is_paid = models.BooleanField(default=False)
    total_money = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"order {self.user}"
