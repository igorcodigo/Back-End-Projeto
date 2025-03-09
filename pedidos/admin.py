from django.contrib import admin
from .models import Product, Order, OrderItem, Review

# Configuração para OrderItem como inline no Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('unit_price', 'subtotal')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name', 'description')
    list_filter = ('price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('total',)
    inlines = [OrderItemInline]
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save()
        for instance in formset.forms:
            if instance.instance.pk:
                instance.instance.order.calculate_total()

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unit_price', 'subtotal')
    list_filter = ('order', 'product')
    search_fields = ('order__id', 'product__name')
    readonly_fields = ('unit_price', 'subtotal')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'product__name', 'comment')
