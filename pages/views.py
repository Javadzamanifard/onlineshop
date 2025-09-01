from django.shortcuts import render
from django.views.generic import TemplateView


class ContactUs(TemplateView):
    template_name = 'pages/contact_us.html'


class AboutUs(TemplateView):
    template_name = 'pages/about.html'


class TermsAndConditions(TemplateView):
    template_name = 'pages/terms_conditions.html'


