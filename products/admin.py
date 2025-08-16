from django.contrib import admin
from .models import Category, Product, Comment

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


