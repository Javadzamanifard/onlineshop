from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'پروفایل'

class CustomUserAdmin(BaseUserAdmin):
    # پروفایل اینلاین را مانند قبل اضافه می‌کنیم
    inlines = (ProfileInline,)

    # ++ این بخش کلیدی و جدید است ++
    # در اینجا، چیدمان فیلدهای صفحه ویرایش کاربر را بازنویسی می‌کنیم
    # تا فیلدهای سفارشی شما هم نمایش داده شوند.
    fieldsets = (
        # بخش اول: اطلاعات ورود (بدون عنوان)
        (None, {'fields': ('username', 'password')}),
        
        # بخش دوم: اطلاعات شخصی با فیلدهای سفارشی شما
        ('اطلاعات شخصی', {'fields': (
            'first_name', 
            'last_name', 
            'email', 
            'phone_number',  # فیلد سفارشی شما
            'national_id',   # فیلد سفارشی شما
        )}),
        
        # بخش سوم: دسترسی‌ها (این بخش از کلاس پایه می‌آید و بهتر است باشد)
        ('دسترسی‌ها', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        
        # بخش چهارم: تاریخ‌های مهم
        ('تاریخ‌های مهم', {'fields': ('last_login', 'date_joined')}),
    )

    # نکته تکمیلی: برای نمایش فیلدها در لیست کاربران
    list_display = ('username', 'email', 'phone_number', 'national_id')

# ثبت نهایی مدل با کلاس ادمین سفارشی
admin.site.unregister(CustomUser)
admin.site.register(CustomUser, CustomUserAdmin)


# admin.site.register(Profile)