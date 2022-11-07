from django.contrib import admin

from .models import CartItem, Address

# Register your models here.
admin.site.register(CartItem)
admin.site.register(Address)
