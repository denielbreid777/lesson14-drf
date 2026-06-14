from rest_framework import serializers
# from .models import Comment, Product, Category, Cart, CartItem, Order, OrderItem
from .models import Category, Product, Comment, Cart, CartItem, Order, OrderItem
from django.contrib.auth.models import User




class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length = 8)
    email = serializers.EmailField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ["username", "password", "email"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        cart, created = Cart.objects.get_or_create(user=user)
        return user 
    
    def update(self, instance, validated_data):
        user = User.objects.update(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

#Памятаємо що якщо нам не вистачає якогось поля, то ми тут в першому класі його мождем создати 
# і потім в fields вказа
# ти. Або можемо одно з полей fields в першому класі перезаписати аби так чи інакше виглядало
class ProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = Product
        fields = ['id', 'user', 'category', 'title', 'price', 'description', 'category_name']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Comment
        fields = ['id', 'user', 'product', 'text', 'is_visible']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)    
    total_price = serializers.ReadOnlyField(source='subtotal')


    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
        read_only_fields = ['id', 'product', 'quantity', 'total_price']

class CartItemCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    class Meta():
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    total_price  = serializers.ReadOnlyField()
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'total_price', 'total_quantity', 'items']



class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'price', 'total_price']
        read_only_fields = fields
    
    

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['user', 'total_price', 'created_at', 'items']
