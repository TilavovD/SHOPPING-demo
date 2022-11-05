from django.db import models
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128)
    sub_categories = models.ManyToManyField(
        'Category',
        related_name='parent_category',
        blank=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to='products')
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )

    cost = models.PositiveIntegerField()
    discount_percent = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} | ${self.cost}"
