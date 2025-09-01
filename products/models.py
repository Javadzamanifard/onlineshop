from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone

from accounts.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=255, )
    slug = models.SlugField(max_length=255, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/product_img', default='products/product_img/default.jpg', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})
        # return reverse('product_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    guest_name = models.CharField(max_length=80, blank=True, null=True, help_text='نام مهمان در صورت عدم لاگین')
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank = True, null = True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    

    class Meta:
        ordering = ['-created_at']
    
    
    def __str__(self):
        if self.user:
            return f'Comment by {self.user} on {self.product}'
        return f'Comment by {self.guest_name or "Anonymous"} on {self.product}'


class WishList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="کاربر")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    
    added_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ اضافه شدن")
    
    def __str__(self):
        return f"{self.product.name} در لیست علاقه‌مندی‌های {self.user.username}"

    class Meta:
        # این خط بسیار مهم است!
        # از اضافه شدن یک محصول تکراری به لیست یک کاربر جلوگیری می‌کند
        unique_together = ('user', 'product')
        verbose_name = "لیست علاقه‌مندی"
        verbose_name_plural = "لیست‌های علاقه‌مندی"