from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUsercreationForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUsercreationForm
    form = CustomUserChangeForm
    list_display = ['username', 'email', ]
    search_fields = ['username']

