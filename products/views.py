from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category
from django.shortcuts import get_object_or_404


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products' # نام متغیری که در تمپلیت استفاده می‌شود
    queryset = Product.objects.all()
    paginate_by = 4


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    # slug_field و slug_url_kwarg را برای استفاده از اسلاگ در URL مشخص می‌کنیم
    slug_field = 'slug'
    slug_url_kwarg = 'slug'



