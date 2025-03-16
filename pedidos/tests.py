from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from decimal import Decimal
from .models import Product, Order, OrderItem, Review

User = get_user_model()

# Testes para Models
class ModelTests(TestCase):
    def setUp(self):
        # Criar usuário para testes
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Criar produtos para testes
        self.product1 = Product.objects.create(
            name='Produto 1',
            description='Descrição do produto 1',
            price=Decimal('10.50')
        )
        
        self.product2 = Product.objects.create(
            name='Produto 2',
            description='Descrição do produto 2',
            price=Decimal('15.75')
        )
        
        # Criar pedido para testes
        self.order = Order.objects.create(
            user=self.user,
            status='Pendente'
        )
        
        # Criar itens de pedido
        self.order_item1 = OrderItem.objects.create(
            order=self.order,
            product=self.product1,
            quantity=2
        )
        
        self.order_item2 = OrderItem.objects.create(
            order=self.order,
            product=self.product2,
            quantity=1
        )
        
        # Calcular total do pedido
        self.order.calculate_total()
        
        # Criar avaliação
        self.review = Review.objects.create(
            user=self.user,
            product=self.product1,
            rating=4,
            comment='Ótimo produto!'
        )
    
    def test_product_creation(self):
        """Testa a criação de um produto"""
        self.assertEqual(self.product1.name, 'Produto 1')
        self.assertEqual(self.product1.price, Decimal('10.50'))
        self.assertEqual(str(self.product1), 'Produto 1')
    
    def test_order_creation(self):
        """Testa a criação de um pedido"""
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.status, 'Pendente')
        self.assertTrue(str(self.order).startswith('Pedido'))
    
    def test_order_item_creation(self):
        """Testa a criação de itens de pedido"""
        self.assertEqual(self.order_item1.product, self.product1)
        self.assertEqual(self.order_item1.quantity, 2)
        self.assertEqual(self.order_item1.unit_price(), Decimal('10.50'))
        self.assertEqual(self.order_item1.subtotal(), Decimal('21.00'))
    
    def test_order_total_calculation(self):
        """Testa o cálculo do total do pedido"""
        # Total deve ser: (2 * 10.50) + (1 * 15.75) = 36.75
        self.assertEqual(self.order.total, Decimal('36.75'))
    
    def test_review_creation(self):
        """Testa a criação de uma avaliação"""
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.product, self.product1)
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.comment, 'Ótimo produto!')

# Testes para APIs
class APITests(APITestCase):
    def setUp(self):
        # Criar usuário para testes
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Criar usuário admin
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword123',
            is_staff=True
        )
        
        # Criar produtos para testes
        self.product1 = Product.objects.create(
            name='Produto 1',
            description='Descrição do produto 1',
            price=Decimal('10.50')
        )
        
        self.product2 = Product.objects.create(
            name='Produto 2',
            description='Descrição do produto 2',
            price=Decimal('15.75')
        )
        
        # Criar pedido para testes
        self.order = Order.objects.create(
            user=self.user,
            status='Pendente'
        )
        
        # Criar itens de pedido
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product1,
            quantity=2
        )
        
        # Calcular total do pedido
        self.order.calculate_total()
        
        # Criar avaliação
        self.review = Review.objects.create(
            user=self.user,
            product=self.product1,
            rating=4,
            comment='Ótimo produto!'
        )
        
        # Cliente API
        self.client = APIClient()
    
    def test_product_list_authenticated(self):
        """Testa listagem de produtos com usuário autenticado"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/pedidos/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_product_list_unauthenticated(self):
        """Testa listagem de produtos sem autenticação"""
        response = self.client.get('/pedidos/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Produtos são públicos
        self.assertTrue(len(response.data) > 0)  # Deve retornar produtos
    
    def test_product_detail(self):
        """Testa detalhes de um produto"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/pedidos/api/products/{self.product1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Produto 1')
    
    def test_product_create(self):
        """Testa criação de um produto"""
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Novo Produto',
            'description': 'Descrição do novo produto',
            'price': '25.99'
        }
        response = self.client.post('/pedidos/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)
    
    def test_product_update(self):
        """Testa atualização de um produto"""
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Produto 1 Atualizado',
            'description': 'Descrição atualizada',
            'price': '12.99'
        }
        response = self.client.put(f'/pedidos/api/products/{self.product1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Produto 1 Atualizado')
        self.assertEqual(response.data['price'], '12.99')
    
    def test_product_partial_update(self):
        """Testa atualização parcial de um produto"""
        self.client.force_authenticate(user=self.user)
        data = {
            'price': '13.99'
        }
        response = self.client.patch(f'/pedidos/api/products/{self.product1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], '13.99')
        self.assertEqual(response.data['name'], 'Produto 1')  # Nome não deve mudar
    
    def test_product_delete(self):
        """Testa exclusão de um produto"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/pedidos/api/products/{self.product1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)
    
    def test_order_list_user(self):
        """Testa listagem de pedidos para usuário normal"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/pedidos/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_order_list_admin(self):
        """Testa listagem de pedidos para admin"""
        # Criar pedido para outro usuário
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword123'
        )
        
        Order.objects.create(
            user=other_user,
            status='Pendente'
        )
        
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/pedidos/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Admin deve ver todos os pedidos (2)
        self.assertEqual(len(response.data), 2)
    
    def test_order_create(self):
        """Testa criação de um pedido"""
        self.client.force_authenticate(user=self.user)
        data = {
            'status': 'Pendente',
            'user': self.user.id
        }
        response = self.client.post('/pedidos/api/orders/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
    
    def test_order_update(self):
        """Testa atualização de um pedido"""
        self.client.force_authenticate(user=self.user)
        data = {
            'status': 'Preparando',  # Usando um status válido do STATUS_CHOICES
            'user': self.user.id
        }
        response = self.client.put(f'/pedidos/api/orders/{self.order.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Preparando')
    
    def test_order_delete(self):
        """Testa exclusão de um pedido"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/pedidos/api/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)
    
    def test_order_item_create(self):
        """Testa criação de um item de pedido"""
        self.client.force_authenticate(user=self.user)
        data = {
            'order': self.order.id,
            'product': self.product2.id,
            'quantity': 3
        }
        response = self.client.post('/pedidos/api/order-items/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar se o total do pedido foi atualizado
        self.order.refresh_from_db()
        # Total deve ser: (2 * 10.50) + (3 * 15.75) = 21.00 + 47.25 = 68.25
        self.assertEqual(self.order.total, Decimal('68.25'))
    
    def test_order_item_update(self):
        """Testa atualização de um item de pedido"""
        self.client.force_authenticate(user=self.user)
        data = {
            'order': self.order.id,
            'product': self.product1.id,
            'quantity': 5
        }
        response = self.client.put(f'/pedidos/api/order-items/{self.order_item.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 5)
        
        # Verificar se o total do pedido foi atualizado
        self.order.refresh_from_db()
        self.assertEqual(self.order.total, Decimal('52.50'))  # 5 * 10.50
    
    def test_order_item_delete(self):
        """Testa exclusão de um item de pedido"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/pedidos/api/order-items/{self.order_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OrderItem.objects.count(), 0)
        
        # Verificar se o total do pedido foi atualizado para zero
        self.order.refresh_from_db()
        self.assertEqual(self.order.total, Decimal('0'))
    
    def test_review_create(self):
        """Testa criação de uma avaliação"""
        self.client.force_authenticate(user=self.user)
        data = {
            'product': self.product2.id,
            'rating': 5,
            'comment': 'Excelente produto!',
            'user': self.user.id
        }
        response = self.client.post('/pedidos/api/reviews/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
    
    def test_review_update(self):
        """Testa atualização de uma avaliação"""
        self.client.force_authenticate(user=self.user)
        data = {
            'product': self.product1.id,
            'rating': 3,
            'comment': 'Atualizando minha avaliação'
        }
        response = self.client.put(f'/pedidos/api/reviews/{self.review.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 3)
        self.assertEqual(response.data['comment'], 'Atualizando minha avaliação')
    
    def test_review_delete(self):
        """Testa exclusão de uma avaliação"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/pedidos/api/reviews/{self.review.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)
    
    def test_reviews_ordering(self):
        """Testa se as avaliações estão sendo retornadas em ordem decrescente de data"""
        # Criar mais algumas avaliações
        Review.objects.create(
            user=self.user,
            product=self.product1,
            rating=5,
            comment='Avaliação mais recente'
        )
        Review.objects.create(
            user=self.user,
            product=self.product1,
            rating=3,
            comment='Avaliação intermediária'
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/pedidos/api/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        
        # Verificar se as datas estão em ordem decrescente
        dates = [review['created_at'] for review in response.data]
        self.assertEqual(dates, sorted(dates, reverse=True))
    
    def test_product_reviews(self):
        """Testa endpoint para listar avaliações de um produto"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/pedidos/api/products/{self.product1.id}/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['rating'], 4)
    
    def test_order_calculate_total(self):
        """Testa endpoint para recalcular o total do pedido"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/pedidos/api/orders/{self.order.id}/calculate_total/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['total']), Decimal('21.00'))
