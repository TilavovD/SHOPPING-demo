from django.contrib import admin

from .models import Category, Product, FavouriteProduct


# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(FavouriteProduct)
