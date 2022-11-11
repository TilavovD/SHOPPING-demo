from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete

from .models import CartItem, Order


@receiver(post_save, sender=Order)
def order_create(sender, instance, created, **kwargs):
    # pass
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


@receiver(pre_save, sender=Order)
def order_create(sender, instance, **kwargs):
    if instance.id is not None:
        user = instance.user
        order = instance
        print('\n\n', 45, '\n\n')

        cart_items = CartItem.objects.filter(user=user, order__isnull=True)
        total_money = 0

        print('\n\n', 41234, '\n\n')
        if cart_items.exists():
            for cart_item in cart_items:
                total_money += cart_item.get_final_price()

                cart_item.order = order
                cart_item.save()
                #
                product = cart_item.product
                product.quantity -= cart_item.amount
                product.save()
            #
            instance.total_money += total_money
            instance.save()
