from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
import random
import datetime

from .serializers import (
    CustomUserSerializer, 
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from .models import CustomUser, PasswordResetCode

# Importar as funções de envio de email
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from email_service.password_reset import send_password_reset_email
from email_service.welcome_email import send_welcome_email

#View para criar usuario com API REST usando Django rest framework
class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CustomUserSerializer
    
    def perform_create(self, serializer):
        user = serializer.save()
        # Enviar email de boas-vindas
        try:
            # Enviar email de boas-vindas
            send_welcome_email(
                email=user.email,
                name=user.first_name or "🥳",
            )
        except Exception as e:
            # Apenas registrar o erro, não impedir a criação do usuário
            print(f"Erro ao enviar email de boas-vindas: {str(e)}")

# Função para gerar código de 6 dígitos
def generate_reset_code():
    return ''.join(random.choices('0123456789', k=6))

# View para solicitar redefinição de senha
class PasswordResetRequestView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = get_user_model().objects.get(email=email)
            
            # Gerar código de 6 dígitos para redefinição
            reset_code = generate_reset_code()
            
            # Definir expiração para 24 horas
            expiry_time = timezone.now() + datetime.timedelta(hours=24)
            
            # Criar novo registro de código de reset
            PasswordResetCode.objects.create(
                user=user,
                email=email,
                code=reset_code,
                expires_at=expiry_time
            )
            
            # Construir a URL de redefinição
            frontend_url = getattr(settings, 'FRONTEND_URL', request.build_absolute_uri('/')[:-1])
            # Atualizar para usar o novo caminho com código
            reset_url = f"{frontend_url}/contas/reset-password/?email={email}&code={reset_code}"
            
            # Enviar email
            try:
                send_password_reset_email(email, reset_url)
                return Response(
                    {"detail": "Email de redefinição de senha enviado com sucesso."},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"detail": f"Erro ao enviar email: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View para confirmar redefinição de senha
@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetConfirmView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetConfirmSerializer
    authentication_classes = []  # Desativa a autenticação para este endpoint

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Senha redefinida com sucesso."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
