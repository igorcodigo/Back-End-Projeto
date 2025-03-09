from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'order-items', views.OrderItemViewSet, basename='orderitem')
router.register(r'reviews', views.ReviewViewSet, basename='review')

urlpatterns = [
    path('api/', include(router.urls)),
]
