from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone

from products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    session_key = models.CharField(max_length=50, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user:
            return f'Cart for {self.user.username}'
        return f'Guest Cart for {self.session_key}'
    
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items', )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    class Meta:
        unique_together = ('cart', 'product', )
    
    
    def __str__(self):
        return f'{self.product.name} * {self.quantity}'
    
    def get_cost(self):
        if self.unit_price is None or self.quantity is None:
            return 0
        return self.unit_price * self.quantity



class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ('percent', 'درصدی'),
        ('fixed', 'مبلغ ثابت'),
    )

    code = models.CharField(max_length=11, unique=True)   # مثل NEWYEAR2025
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    
    # نوع تخفیف: درصدی یا مبلغ ثابت
    discount_type = models.CharField(
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES,
        default='percent'
    )
    
    # مقدار تخفیف: می‌تونه درصد یا مبلغ باشه
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    usage_limit = models.PositiveIntegerField(null=True, blank=True)  # محدودیت تعداد استفاده (مثلاً 100 بار)
    used_count = models.PositiveIntegerField(default=0)  # چند بار استفاده شده
    
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-valid_from']

    def __str__(self):
        return self.code

    def is_valid(self):
        """چک کنه کوپن معتبره یا نه"""
        now = timezone.now()
        if not self.active:
            return False
        if self.valid_from > now or self.valid_to < now:
            return False
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False
        return True

    def get_discount_amount(self, total_price):
        """مقدار تخفیف رو بر اساس نوع کوپن حساب کنه"""
        if self.discount_type == 'percent':
            return (self.discount_value / 100) * total_price
        elif self.discount_type == 'fixed':
            return min(self.discount_value, total_price)  # تخفیف از کل بیشتر نشه
        return 0

    def apply_discount(self, total_price):
        """اعمال تخفیف روی قیمت نهایی"""
        if not self.is_valid():
            return total_price
        discount = self.get_discount_amount(total_price)
        return total_price - discount
