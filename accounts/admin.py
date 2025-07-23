from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUsercreationForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUsercreationForm
    form = CustomUserChangeForm
    list_display = ['username', 'email', 'national_id', 'phone_number', ]
    search_fields = ['username', 'national_id', ]
    
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                'fields': ('national_id', 'phone_number', )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                'fields': ('national_id', 'phone_number', )
            },
        ),
    )
