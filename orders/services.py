from django.core.mail import send_mail
from django.db import transaction
from rest_framework.exceptions import ValidationError

from cart.models import CartItem
from orders.models import Order, OrderItem


@transaction.atomic
def create_order_from_cart(user):
    cart_items = CartItem.objects.select_related('product').filter(user=user)

    if not cart_items.exists():
        raise ValidationError('Корзина пуста')

    total_price = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    if user.balance < total_price:
        raise ValidationError('Недостаточно средств на балансе')

    for item in cart_items:
        if item.product.stock < item.quantity:
            raise ValidationError(
                f'Недостаточно товара на складе: {item.product.name}'
            )

    order = Order.objects.create(
        user=user,
        total_price=total_price,
    )

    for item in cart_items:
        product = item.product

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item.quantity,
            price=product.price,
        )

        product.stock -= item.quantity
        product.save()

    user.balance -= total_price
    user.save()

    cart_items.delete()

    send_mail(
        subject=f'Заказ #{order.id} успешно создан',
        message=(
            f'Здравствуйте, {user.username}!\n\n'
            f'Ваш заказ #{order.id} успешно создан.\n'
            f'Сумма заказа: {order.total_price}.\n\n'
            f'Спасибо за покупку!'
        ),
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return order
