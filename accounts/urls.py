from django.urls import path

from .views import homeview, CustomSignUpView, CustomPasswordChangeView

urlpatterns = [
    path('home/', homeview, name='home'),
    path('signup/', CustomSignUpView.as_view(), name='signup'),
    path('accounts/password/change/', CustomPasswordChangeView.as_view(), name='account_change_password'),
]
