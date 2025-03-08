import resend
from dotenv import load_dotenv
import os

# Carregar as variáveis do arquivo .env
load_dotenv()

# Encontra a localização da pasta atual para facilitar a conexão com caminhos de arquivos
current_directory = os.path.dirname(os.path.abspath(__file__))

# Obter a chave API do arquivo .env
resend.api_key = os.getenv('RESEND_API_KEY')

def send_welcome_email(email, name):
    """
    Envia um email de boas-vindas para o usuário recém-cadastrado.
    
    Args:
        email (str): O endereço de email do usuário
        name (str): O nome do usuário
    
    Returns:
        dict: Resposta da API Resend
    """
    # Verificar se a chave API foi carregada corretamente
    if not resend.api_key:
        raise ValueError("Erro: RESEND_API_KEY não encontrada no arquivo .env")
    
    # Construir o caminho absoluto para o arquivo HTML
    html_file_path = os.path.join(current_directory, 'templates', 'welcome_template.html')
    
    # Ler o arquivo HTML
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Substituir os placeholders pelos valores reais
    html_content = html_content.replace('{{ name }}', name)
    
    try:
        # Enviar o e-mail utilizando o conteúdo do arquivo HTML
        response = resend.Emails.send({
            "from": "no-reply@miraidev.com.br",  # Use um domínio verificado no Resend
            "to": [email],
            "subject": "Bem-vindo(a) à nossa plataforma!",
            "html": html_content
        })
        return response
    except Exception as e:
        raise Exception(f"Erro ao enviar email: {e}") 