from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


from products.models import Product 


class Order(models.Model):
    # وضعیت‌های مختلف یک سفارش
    STATUS_CHOICES = (
        ('pending', 'در انتظار پرداخت'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
        ('cancelled', 'لغو شده'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name="کاربر")
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders', verbose_name="کاربر")
    
    # اطلاعات مشتری در لحظه خرید (کپی می‌شود تا با تغییر پروفایل کاربر، سابقه از بین نرود)
    first_name  = models.CharField(max_length=100, verbose_name="نام")
    last_name   = models.CharField(max_length=100, verbose_name="نام خانوادگی")
    email       = models.EmailField(verbose_name="ایمیل", blank=True, null=True)
    phone       = models.CharField(max_length=11, verbose_name="شماره همراه")
    address     = models.CharField(max_length=255, verbose_name="آدرس")
    postal_code = models.CharField(max_length=20, verbose_name="کد پستی")
    city        = models.CharField(max_length=100, verbose_name="شهر")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    status  = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت سفارش")
    is_paid = models.BooleanField(default=False, verbose_name="پرداخت شده؟")

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش‌ها'

    def __str__(self):
        return f'سفارش #{self.id} by {self.user.username}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())



class OrderItem(models.Model):
    order   = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="سفارش")
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name="محصول")
    
    # قیمت محصول در لحظه خرید (چون ممکن است قیمت محصول در آینده تغییر کند)
    price = models.PositiveIntegerField(verbose_name="قیمت")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity