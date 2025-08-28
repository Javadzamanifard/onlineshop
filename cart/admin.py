from django.contrib import admin

from .models import Cart, CartItem, Coupon


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'unit_price', 'get_cost')
    fields = ('product', 'quantity', 'unit_price', 'get_cost')

    def get_cost(self, obj):
        return obj.get_cost()
    get_cost.short_description = 'مجموع'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'created_at', 'updated_at', 'items_preview', 'get_total_price')
    list_display_links = ('id', 'user')  # لینک ورود به جزئیات
    inlines = [CartItemInline]

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'جمع کل'

    def items_preview(self, obj):
        """نمایش خلاصه آیتم‌ها در لیست Cartها"""
        items = obj.items.all()
        if not items:
            return "—"
        return ", ".join([f"{item.product.name} × {item.quantity}" for item in items])
    items_preview.short_description = 'آیتم‌ها'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'valid_from', 'valid_to', 'active', 'used_count')
    list_filter = ('active', 'discount_type')
    search_fields = ('code',)

