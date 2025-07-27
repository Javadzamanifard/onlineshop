from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError

from allauth.account.forms import SignupForm

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        #---------------------------
        #1
        # fields = UserChangeForm.Meta.fields + ('national_id', 'phone_number', )
        #2
        fields = ('username', 'email','national_id', 'phone_number', )



class CustomUsercreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        #---------------------------
        #1
        # fields = UserCreationForm.Meta.fields + ('national_id', 'phone_number', )
        #2
        fields = ('username', 'email', 'national_id', 'phone_number', )


class CustomSignUpForm(SignupForm):
    phone_number = forms.CharField(max_length=11, label='شماره همراه', widget=forms.TextInput(attrs={'placeholder':'09123456789'}))
    national_id = forms.CharField(max_length=10, label='شماره ملی', widget=forms.TextInput(attrs={'placeholder':'1234567890'}))
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit():
            raise ValidationError('شماره همراه باید فقط شامل اعداد باشد')
        if len(phone_number) != 11:
            raise ValidationError('شماره همراه باید 11 رقم باشد')
        return phone_number
    
    def clean_national_id(self):
        national_id = self.cleaned_data['national_id']
        if not national_id.isdigit():
            raise ValidationError('شماره ملی باید فقط شامل اعداد باشد')
        if len(national_id) != 10:
            raise ValidationError('شماره ملی باید 10 رقم باشد')
        return national_id
    
    def save(self, request):
        user = super().save(request)
        user.phone_number = self.cleaned_data['phone_number']
        user.national_id = self.cleaned_data['national_id']
        user.save()
        return user