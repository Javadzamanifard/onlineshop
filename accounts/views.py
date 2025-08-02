from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from allauth.account.views import PasswordChangeView
from django.contrib import messages

from .forms import CustomSignUpForm


def homeview(request):
    return render(request, 'accounts/home.html')


class CustomSignUpView(generic.CreateView):
    form_class = CustomSignUpForm
    template_name = 'account/signup.html'
    context_object_name = 'form'
    success_url = reverse_lazy('home')


class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, 'رمز عبور با موفیت تغییر یافت')
        return super().form_valid(form)

