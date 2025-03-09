from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product, Order, OrderItem, Review
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer, ReviewSerializer

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Retorna todas as avaliações de um produto específico"""
        product = self.get_object()
        reviews = Review.objects.filter(product=product)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtra pedidos pelo usuário logado, a menos que seja staff"""
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)
    
    def perform_create(self, serializer):
        """Associa o usuário logado ao pedido"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def calculate_total(self, request, pk=None):
        """Recalcula o total do pedido"""
        order = self.get_object()
        order.calculate_total()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtra itens de pedido pelo usuário logado, a menos que seja staff"""
        user = self.request.user
        if user.is_staff:
            return OrderItem.objects.all()
        return OrderItem.objects.filter(order__user=user)
    
    def perform_create(self, serializer):
        """Salva o item e recalcula o total do pedido"""
        item = serializer.save()
        item.order.calculate_total()
    
    def perform_update(self, serializer):
        """Atualiza o item e recalcula o total do pedido"""
        item = serializer.save()
        item.order.calculate_total()
    
    def perform_destroy(self, instance):
        """Remove o item e recalcula o total do pedido"""
        order = instance.order
        instance.delete()
        order.calculate_total()

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtra avaliações pelo usuário logado, a menos que seja staff"""
        user = self.request.user
        if user.is_staff:
            return Review.objects.all()
        return Review.objects.filter(user=user)
    
    def perform_create(self, serializer):
        """Associa o usuário logado à avaliação"""
        serializer.save(user=self.request.user)
