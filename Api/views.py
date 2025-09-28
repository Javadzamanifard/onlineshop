from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Category, Product, Comment, WishList
from .serializers import (
    CategorySerializer, ProductSerializer,
    CommentListSerializer, CommentCreateSerializer, WishListSerializer
)
from accounts.models import CustomUser 


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_staff


class IsAuthenticatedAndOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'DELETE']:
            return request.user and request.user.is_authenticated
        return True


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().select_related('category')
    filterset_fields = ['category', 'price'] 
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'


class CommentListCreateAPIView(mixins.ListModelMixin, 
                                mixins.CreateModelMixin, 
                                viewsets.GenericViewSet):
    queryset = Comment.objects.filter(is_active=True) 
    permission_classes = [permissions.AllowAny] 
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentListSerializer

    def get_queryset(self):
        product_slug = self.kwargs.get('product_slug')
        product = get_object_or_404(Product, slug=product_slug)
        return self.queryset.filter(product=product, parent__isnull=True) 
        
    def perform_create(self, serializer):
        """Set the user for the comment if authenticated."""
        user = self.request.user if self.request.user.is_authenticated else None
        product_slug = self.kwargs.get('product_slug')
        product = get_object_or_404(Product, slug=product_slug)
        
        serializer.save(user=user, product=product, is_active=True)


class CommentRetrieveUpdateDestroyAPIView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    permission_classes = [IsOwnerOrAdmin] 
    
    def get_serializer_class(self):
        return CommentListSerializer


class WishListViewSet(viewsets.ModelViewSet):
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticatedAndOwner] 
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return WishList.objects.filter(user=self.request.user).select_related('product')
        return WishList.objects.none()
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)