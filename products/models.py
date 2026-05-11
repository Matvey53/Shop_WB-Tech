from decimal import Decimal

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=254, verbose_name='Наименование товара')

    description = models.TextField(verbose_name='Описание товара')

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name='Цена товара',
    )

    stock = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество на складе',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления товара',
    )

    def __str__(self):
        return self.name
