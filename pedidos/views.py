from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product, Order, OrderItem, Review
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer, ReviewSerializer
from django.contrib.auth import get_user_model

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Retorna todas as avaliações de um produto específico"""
        product = self.get_object()
        reviews = Review.objects.filter(product=product)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()  # Retorna todos os pedidos sem filtro
    
    def perform_create(self, serializer):
        """Cria um pedido, usando o usuário atual se autenticado, ou o primeiro usuário do sistema"""
        User = get_user_model()
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            # Assume o primeiro usuário do sistema para pedidos não autenticados
            default_user = User.objects.first()
            if default_user:
                serializer.save(user=default_user)
            else:
                serializer.save() 
    
    @action(detail=True, methods=['post'])
    def calculate_total(self, request, pk=None):
        """Recalcula o total do pedido"""
        order = self.get_object()
        order.calculate_total()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()  # Retorna todos os itens sem filtro
    
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
    queryset = Review.objects.all().order_by('-created_at')  # Ordenar por data de criação decrescente
    
    def perform_create(self, serializer):
        """Cria uma avaliação, associando ao usuário autenticado se disponível"""
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()  # Permite criar sem usuário (será null)
