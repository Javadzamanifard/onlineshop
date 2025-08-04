from django.urls import path
from .views import ProductListView, ProductDetailView

app_name = 'product' # برای namespacing

urlpatterns = [
    # آدرس برای لیست محصولات: /products/
    path('', ProductListView.as_view(), name='product_list'),
    # آدرس برای جزئیات یک محصول: /products/some-product-slug/
    path('<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),
]