from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete

from .models import CartItem, Order


@receiver(post_save, sender=Order)
def sponsorstudent_create(sender, instance, created, **kwargs):
    if created:
        user = instance.user

        cart_items = CartItem.objects.filter(user=user, order__isnull=True)
        total_money = 0

        for cart_item in cart_items:
            total_money += cart_item.get_final_price()

            cart_item.order = instance
            cart_item.save()

            product = cart_item.product
            product.quantity -= cart_item.amount
            product.save()

        instance.total_money = total_money
        instance.save()
