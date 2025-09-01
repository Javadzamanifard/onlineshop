from django.urls import path
from .views import ProductListView, product_detail_view, toggle_wishlist_view, WishlistPageView

# app_name = 'products'
urlpatterns = [
    # آدرس برای لیست محصولات: /products/
    path('', ProductListView.as_view(), name='product_list'),
    # آدرس برای جزئیات یک محصول: /products/some-product-slug/
    # path('<int:pk>/', product_detail, name='product_detail'),
    # path('<slug:slug>/', product_detail_view, name='product_detail'),
    path('<int:pk>/', product_detail_view, name='product_detail'),
    
    path('toggle-wishlist/', toggle_wishlist_view, name='toggle_wishlist'),
    path('my-wishlist/', WishlistPageView.as_view(), name='wishlist_page'),
    
]