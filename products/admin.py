from django.contrib import admin
from .models import Category, Product, Comment, WishList

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} # اسلاگ به صورت خودکار از روی نام پر می‌شود


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'created_at']
    list_filter = ['created_at', 'category']
    list_editable = ['price', 'stock',] # امکان ویرایش مستقیم از لیست
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'content', 'is_active']



@admin.register(WishList)
class WishlistAdmin(admin.ModelAdmin):
    """
    کلاس برای سفارشی‌سازی نمایش مدل Wishlist در پنل ادمین.
    """
    
    # ستون‌هایی که در لیست نمایش داده می‌شوند
    list_display = ('user', 'product', 'added_date')
    
    # فیلدهایی که بر اساس آن‌ها می‌توان لیست را فیلتر کرد
    list_filter = ('added_date', 'user')
    
    # فیلدهایی که می‌توان بر اساس آن‌ها جستجو انجام داد
    # برای جستجو در مدل‌های دیگر (ForeignKey) از __ استفاده می‌کنیم
    search_fields = ('user__username', 'product__name')
    
    # تاریخ اضافه شدن نباید دستی تغییر کند، پس آن را فقط خواندنی می‌کنیم
    readonly_fields = ('added_date',)

    # برای بهبود عملکرد در پنل ادمین، وقتی تعداد کاربران و محصولات زیاد است
    autocomplete_fields = ['user', 'product']
