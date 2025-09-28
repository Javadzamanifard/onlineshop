from rest_framework import serializers

from products.models import Category, Comment, Product, WishList



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        queryset=Category.objects.all(),
        source='category',
        read_only=True,
    )
    
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    
    class Meta:
        model = Product
        fields = '__all__'
        
        
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive.")
        return value
    
    def validate_name(self, value):
        if not value or len(value) < 5:
            raise serializers.ValidationError("Name must be at least 5 characters long.")
        return value



class CommentListSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ('id', 'author_name', 'content', 'created_at', 'parent', 'replies')
        read_only_fields = ('id', 'author_name', 'created_at', 'parent', 'replies')

    def get_author_name(self, obj):
        if obj.user:
            return obj.user.username 
        return obj.guest_name or "Anonymous"
        
    def get_replies(self, obj):
        active_replies = obj.replies.filter(is_active=True)
        return CommentListSerializer(active_replies, many=True, context=self.context).data


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('product', 'content', 'guest_name', 'parent')
        
    def validate(self, data):
        request = self.context.get('request', None)
        user = request.user if request and request.user.is_authenticated else None
        
        if not user and not data.get('guest_name'):
            raise serializers.ValidationError("Either log in or provide a guest name.")
        return data



class WishListSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name') 
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = WishList
        fields = ('id', 'user', 'product', 'product_name', 'added_date', 'user_username')
        read_only_fields = ('user', 'added_date', 'product_name', 'user_username')
        
    def validate(self, data):
        request = self.context.get('request', None)
        user = request.user if request and request.user.is_authenticated else None
        
        if not user:
            raise serializers.ValidationError("User must be logged in to add to wishlist.")
            
        product = data.get('product')
        
        if WishList.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError({'product': "This product is already in your wishlist."})
            
        return data


