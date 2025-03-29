from rest_framework import serializers
from .models import Product, Order, OrderItem, Review
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_name', 'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['unit_price', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'username', 'status', 'total', 'created_at', 'items']
        read_only_fields = ['total', 'created_at']
    
    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        return order
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.calculate_total()
        return instance

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'name', 'username', 'product', 'product_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']
    
    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        elif obj.name:
            return obj.name
        return "Usuário Anônimo"
