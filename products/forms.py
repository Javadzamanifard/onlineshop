from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'guest_name', 'parent']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'متن کامنت شما…'}),
            'guest_name': forms.TextInput(attrs={'placeholder': 'نام شما (اختیاری)'}),
            'parent': forms.HiddenInput(attrs={'id' : 'parent_id'}),
        }
