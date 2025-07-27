from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomSignUpForm


def homeview(request):
    return render(request, 'accounts/home.html')


class CustomSignUpView(generic.CreateView):
    form_class = CustomSignUpForm
    template_name = 'account/signup.html'
    context_object_name = 'form'
    success_url = reverse_lazy('home')

