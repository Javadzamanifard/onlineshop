from django import forms



class CartForm(forms.Form):
    QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 31)]
    
    quantity = forms.TypedChoiceField(choices = QUANTITY_CHOICES, coerce = int)
    override_quantity = forms.BooleanField(required = False, widget = forms.HiddenInput)


#2
# class CartForm(forms.Form):
#     quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'form-control text-center'}))
#     override_quantity = forms.BooleanField(required=False, widget=forms.HiddenInput)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'کد تخفیف را وارد کنید',
        'aria-label': 'Recipient\'s username', 
        'aria-describedby': 'button-addon2'
    }))