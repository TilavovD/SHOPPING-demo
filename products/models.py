from django.db import models
from django.utils import timezone

from users.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128)
    parent_category = models.ForeignKey(
        'Category',
        related_name='child_categories',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128)
    sub_name = models.CharField(max_length=128)
    image = models.ImageField(upload_to='products')
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )

    price = models.PositiveIntegerField()
    discount_percent = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    volume = models.PositiveIntegerField()

    artikul_number = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} | ${self.price}"

    def get_price_after_discount(self):
        return self.price * (100 - self.discount_percent) / 100


class FavouriteProduct(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favourite_products',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='users_liked_by',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.product.name} liked by {self.user}"
