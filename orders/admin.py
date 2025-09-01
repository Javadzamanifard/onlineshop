from django.contrib import admin

from .models import Order, OrderItem


class OredrItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('user', 'first_name', 'last_name', 'address', 'phone', 'is_paid', )
    ordering = ('-created_at', )
    inlines = [OredrItemInline]
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ('product', 'price', 'quantity', )
