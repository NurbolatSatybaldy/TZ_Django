from django.contrib import admin
from .models import Item, Order, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Админ-панель для товаров"""
    list_display = ('name', 'price', 'currency', 'description')
    list_filter = ('currency',)
    search_fields = ('name', 'description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Админ-панель для заказов"""
    list_display = ('id', 'get_items_count', 'get_total_price', 'discount', 'tax')
    filter_horizontal = ('items',)

    def get_items_count(self, obj):
        """Количество товаров в заказе"""
        return obj.items.count()
    get_items_count.short_description = "Количество товаров"

    def get_total_price(self, obj):
        """Общая стоимость заказа"""
        return f"{obj.get_total_price()} {obj.get_currency()}"
    get_total_price.short_description = "Общая стоимость"


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """Админ-панель для скидок"""
    list_display = ('name', 'coupon_id')
    search_fields = ('name', 'coupon_id')


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    """Админ-панель для налогов"""
    list_display = ('name', 'tax_rate_id')
    search_fields = ('name', 'tax_rate_id')

