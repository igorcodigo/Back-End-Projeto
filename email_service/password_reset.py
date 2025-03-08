import resend
from dotenv import load_dotenv
import os

# Carregar as variáveis do arquivo .env
load_dotenv()

# Encontra a localização da pasta atual para facilitar a conexão com caminhos de arquivos
current_directory = os.path.dirname(os.path.abspath(__file__))

# Obter a chave API do arquivo .env
resend.api_key = os.getenv('RESEND_API_KEY')
# Compara o valor convertido para minúsculas com a string 'true'.
# Se for '1', 'true', 'yes', o resultado será True.
app_exclusive = os.getenv('APP_EXCLUSIVE', 'False').strip().lower() in ('1', 'true', 'yes')
def send_password_reset_email(email, reset_url):
    """
    Envia um email de recuperação de senha para o usuário.
    
    Args:
        email (str): O endereço de email do usuário
        reset_url (str): A URL para redefinir a senha
    
    Returns:
        dict: Resposta da API Resend
    """
    # Verificar se a chave API foi carregada corretamente
    if not resend.api_key:
        raise ValueError("Erro: RESEND_API_KEY não encontrada no arquivo .env")
    
    # Extrair o código de reset da URL
    import urllib.parse
    parsed_url = urllib.parse.urlparse(reset_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    reset_code = query_params.get('code', [''])[0]
    
    # Construir o caminho absoluto para o arquivo HTML
    html_file_path = os.path.join(current_directory, 'templates', 'password_reset_template.html')
    
    # Ler o arquivo HTML
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Substituir os placeholders pela URL real e código
    html_content = html_content.replace('{{ reset_code }}', reset_code)
    
    # Condicional para incluir ou não o botão e link de redefinição de senha
    if app_exclusive:
        # Se for exclusivo para app, remove o botão e o link
        html_content = html_content.replace('{{ RESET_BUTTON_PLACEHOLDER }}', '')
        html_content = html_content.replace('{{ RESET_LINK_PLACEHOLDER }}', '')
    else:
        # Se não for exclusivo para app, inclui o botão e o link
        reset_button = f'<div style="text-align: center;"><a href="{reset_url}" style="display: inline-block; padding: 10px 20px; margin: 20px 0; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">Redefinir Senha</a></div>'
        reset_link = f'<p>Ou copie e cole o seguinte link no seu navegador:</p><p style="word-break: break-all;">{reset_url}</p>'
        
        html_content = html_content.replace('{{ RESET_BUTTON_PLACEHOLDER }}', reset_button)
        html_content = html_content.replace('{{ RESET_LINK_PLACEHOLDER }}', reset_link)
    
    try:
        # Enviar o e-mail utilizando o conteúdo do arquivo HTML
        response = resend.Emails.send({
            "from": "no-reply@miraidev.com.br",  # Use um domínio verificado no Resend
            "to": [email],
            "subject": "Recuperação de Senha",
            "html": html_content
        })
        return response
    except Exception as e:
        raise Exception(f"Erro ao enviar email: {e}") 