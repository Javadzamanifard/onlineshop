from django import forms

from accounts.models import CustomUser
from .models import Profile

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'national_id', ]
        help_texts = {
            'email': 'ایمیل باید منحصر به فرد باشد.',
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
