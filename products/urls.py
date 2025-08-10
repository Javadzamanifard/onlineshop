from django.urls import path
from .views import ProductListView, ProductDetailView

urlpatterns = [
    # آدرس برای لیست محصولات: /products/
    path('', ProductListView.as_view(), name='product_list'),
    # آدرس برای جزئیات یک محصول: /products/some-product-slug/
    # path('<int:pk>/', product_detail, name='product_detail'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]