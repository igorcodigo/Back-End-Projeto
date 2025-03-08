from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import CreateUserView, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Autenticação tradicional baseada em sessão do Django
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('api/users/create/', CreateUserView.as_view(), name='create_user'),
    
    # Endpoints para redefinição de senha
    path('api/password/reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('api/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Template para redefinição de senha (agora usando query parameters)
    path('reset-password/', 
         TemplateView.as_view(template_name='password_reset_confirm.html'), 
         name='password_reset_confirm_page'),
]
