from django.urls import path

from .views import homeview, CustomSignUpView

urlpatterns = [
    path('home/', homeview, name='home'),
    path('signup/', CustomSignUpView.as_view(), name='signup'),
]
