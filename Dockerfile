# Usar a imagem oficial do Python
FROM python:3.11

# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies 
# Instalação de dependências do sistema não necessariamente necessárias:
# Se você não estiver utilizando pacotes que exigem gcc, essa etapa 
# é desnecessária e pode aumentar o tamanho da imagem. 
RUN apt-get update && apt-get install -y gcc

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
