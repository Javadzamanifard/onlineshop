from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'wishlist', views.WishListViewSet, basename='wishlist')


urlpatterns = [
    path('', include(router.urls)), 
    
    
    path(
        'products/<slug:product_slug>/comments/', 
        views.CommentListCreateAPIView.as_view({'get': 'list', 'post': 'create'}), 
        name='product-comment-list-create'
    ),
    
    path(
        'comments/<int:pk>/', 
        views.CommentRetrieveUpdateDestroyAPIView.as_view({
            'get': 'retrieve', 
            'put': 'update', 
            'patch': 'partial_update', 
            'delete': 'destroy'
        }), 
        name='comment-detail'
    ),
]