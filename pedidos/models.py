from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Preço unitário do produto
    image_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Preparando', 'Em Preparação'),
        ('Entregue', 'Entregue'),
        ('Cancelado', 'Cancelado'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Total do pedido
    created_at = models.DateField(auto_now_add=True)  # Data do pedido

    def calculate_total(self):
        """Atualiza o total do pedido com base nos itens."""
        self.total = sum(item.subtotal() for item in self.items.all())
        self.save()

    def __str__(self):
        username = self.user.username if self.user else "Usuário Anônimo"
        return f"Pedido {self.id} - {username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def unit_price(self):
        """Retorna o preço unitário baseado no produto"""
        return self.product.price

    def subtotal(self):
        """Calcula o subtotal do item"""
        return self.quantity * self.unit_price()

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Pedido {self.order.id})"

    class Meta:
        unique_together = ('order', 'product')  # Evita duplicação do mesmo produto no pedido

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Nota (1 a 5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)  # Data da avaliação

    def __str__(self):
        username = self.user.username if self.user else "Usuário Anônimo"
        return f"Avaliação {self.rating} - {self.product.name} ({username})"
