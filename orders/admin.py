from django.contrib import admin

from .models import CartItem, Address, Order

# Register your models here.
admin.site.register(CartItem)
admin.site.register(Address)
admin.site.register(Order)
