from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model



class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        #---------------------------
        #1
        # fields = UserChangeForm.Meta.fields
        #2
        fields = ('username', 'email',)



class CustomUsercreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        #---------------------------
        #1
        # fields = UserCreationForm.Meta.fields
        #2
        fields = ('username', 'email',)
