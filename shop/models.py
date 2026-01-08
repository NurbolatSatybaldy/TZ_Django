from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Item(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Цена"
    )
    currency = models.CharField(
        max_length=3,
        default="USD",
        choices=[("USD", "USD"), ("RUB", "RUB")],
        verbose_name="Валюта"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class Discount(models.Model):
    """Модель скидки для Stripe"""
    name = models.CharField(max_length=255, verbose_name="Название")
    coupon_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="ID купона в Stripe"
    )

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    def __str__(self):
        return self.name


class Tax(models.Model):
    """Модель налога для Stripe"""
    name = models.CharField(max_length=255, verbose_name="Название")
    tax_rate_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="ID налоговой ставки в Stripe"
    )

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"

    def __str__(self):
        return self.name


class Order(models.Model):
    """Модель заказа, объединяющая несколько товаров"""
    items = models.ManyToManyField(Item, verbose_name="Товары")
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Скидка"
    )
    tax = models.ForeignKey(
        Tax,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Налог"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.id}"

    def get_total_price(self):
        """Вычисляет общую стоимость всех товаров в заказе"""
        return sum(item.price for item in self.items.all())

    def get_currency(self):
        """Возвращает валюту заказа"""
        first_item = self.items.first()
        return first_item.currency if first_item else "USD"

