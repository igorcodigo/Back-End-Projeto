
## Produtos

### Listar todos os produtos
- **URL**: `/pedidos/api/products/`
- **Método**: GET
- **Resposta de Sucesso**:
  - **Código**: 200 OK
  - **Conteúdo**: Lista de produtos

### Obter detalhes de um produto
- **URL**: `/pedidos/api/products/{id}/`
- **Método**: GET
- **Resposta de Sucesso**:
  - **Código**: 200 OK
  - **Conteúdo**: Detalhes do produto

### Criar um novo produto
- **URL**: `/pedidos/api/products/`
- **Método**: POST
- **Dados**:
  ```json
  {
    "name": "Nome do Produto",
    "description": "Descrição do produto",
    "price": "19.99",
    "image_url": "https://exemplo.com/imagem.jpg"
  }
  ```
- **Resposta de Sucesso**:
  - **Código**: 201 Created
  - **Conteúdo**: Detalhes do produto criado

### Atualizar um produto
- **URL**: `/pedidos/api/products/{id}/`
- **Método**: PUT
- **Dados**:
  ```json
  {
    "name": "Nome Atualizado",
    "description": "Descrição atualizada",
    "price": "29.99",
    "image_url": "https://exemplo.com/nova-imagem.jpg"
  }
  ```
- **Resposta de Sucesso**:
  - **Código**: 200 OK
  - **Conteúdo**: Detalhes do produto atualizado

### Atualizar parcialmente um produto
- **URL**: `/pedidos/api/products/{id}/`
- **Método**: PATCH
- **Dados**:
  ```json
  {
    "price": "24.99"
  }
  ```
- **Resposta de Sucesso**:
  - **Código**: 200 OK
  - **Conteúdo**: Detalhes do produto atualizado

### Excluir um produto
- **URL**: `/pedidos/api/products/{id}/`
- **Método**: DELETE
- **Resposta de Sucesso**:
  - **Código**: 204 No Content

### Listar avaliações de um produto
- **URL**: `/pedidos/api/products/{id}/reviews/`
- **Método**: GET
- **Resposta de Sucesso**:
  - **Código**: 200 OK
  - **Conteúdo**: Lista de avaliações do produto

## Pedidos

### Listar todos os pedidos
- **URL**: `/pedidos/api/orders/`
- **Método**: GET
- **Observação**: Usuários comuns verão apenas seus próprios pedidos. Administradores verão todos os pedidos.
- **Resposta de Sucesso**:
  - **Código**: 200 OK
  - **Conteúdo**: Lista de pedidos

### Obter detalhes de um pedido
- **URL**: `/pedidos/api/orders/{id}/`
- **Método**: GET
- **Resposta de Sucesso**:
  - **Código**: 200 OK
  - **Conteúdo**: Detalhes do pedido, incluindo itens

### Criar um novo pedido
- **URL**: `/pedidos/api/orders/`
- **Método**: POST
- **Dados**:
  ```json
  {
    "status": "Pendente"
  }
  ```
- **Observação**: O usuário é automaticamente associado ao pedido logado.
- **Resposta de Sucesso**:
  - **Código**: 201 Created
  - **Conteúdo**: Detalhes do pedido criado

### Atualizar um pedido
- **URL**: `/pedidos/api/orders/{id}/`
- **Método**: PUT
- **Dados**:
  ```json
  {
    "status": "Preparando"
  }
  ```
- **Resposta de Sucesso**:
  - **Código**: 200 OK
  - **Conteúdo**: Detalhes do pedido atualizado

### Atualizar parcialmente um pedido
- **URL**: `/pedidos/api/orders/{id}/`
- **Método**: PATCH
- **Dados**:
  ```json
  {
    "status": "Entregue"
  }
  ```
- **Resposta de Sucesso**:
  - **Código**: 200 OK
  - **Conteúdo**: Detalhes do pedido atualizado

### Excluir um pedido
- **URL**: `/pedidos/api/orders/{id}/`
- **Método**: DELETE
- **Resposta de Sucesso**:
  - **Código**: 204 No Content

### Recalcular total do pedido
- **URL**: `/pedidos/api/orders/{id}/calculate_total/`
- **Método**: POST
- **Resposta de Sucesso**:
  - **Código**: 200 OK
  - **Conteúdo**: Detalhes do pedido com total atualizado

## Itens de Pedido

### Listar todos os itens de pedido
- **URL**: `/pedidos/api/order-items/`
- **Método**: GET
- **Observação**: Usuários comuns verão apenas itens de seus próprios pedidos. Administradores verão todos os itens.
- **Resposta de Sucesso**:
  - **Código**: 200 OK
  - **Conteúdo**: Lista de itens de pedido

### Obter detalhes de um item de pedido
- **URL**: `/pedidos/api/order-items/{id}/`
- **Método**: GET
- **Resposta de Sucesso**:
  - **Código**: 200 OK
  - **Conteúdo**: Detalhes do item de pedido

### Adicionar um item ao pedido
- **URL**: `/pedidos/api/order-items/`
- **Método**: POST
- **Dados**:
  ```json
  {
    "order": 1,
    "product": 2,
    "quantity": 3
  }
  ```
- **Observação**: O total do pedido é automaticamente recalculado.
- **Resposta de Sucesso**:
  - **Código**: 201 Created
  - **Conteúdo**: Detalhes do item de pedido criado

### Atualizar um item de pedido
- **URL**: `/pedidos/api/order-items/{id}/`
- **Método**: PUT
- **Dados**:
  ```json
  {
    "order": 1,
    "product": 2,
    "quantity": 5
  }
  ```
- **Observação**: O total do pedido é automaticamente recalculado.
- **Resposta de Sucesso**:
  - **Código**: 200 OK
  - **Conteúdo**: Detalhes do item de pedido atualizado

### Atualizar parcialmente um item de pedido
- **URL**: `/pedidos/api/order-items/{id}/`
- **Método**: PATCH
- **Dados**:
  ```json
  {
    "quantity": 4
  }
  ```
- **Observação**: O total do pedido é automaticamente recalculado.
- **Resposta de Sucesso**:
  - **Código**: 200 OK
  - **Conteúdo**: Detalhes do item de pedido atualizado

### Excluir um item de pedido
- **URL**: `/pedidos/api/order-items/{id}/`
- **Método**: DELETE
- **Observação**: O total do pedido é automaticamente recalculado.
- **Resposta de Sucesso**:
  - **Código**: 204 No Content

## Avaliações

### Listar todas as avaliações
- **URL**: `/pedidos/api/reviews/`
- **Método**: GET
- **Observação**: Usuários comuns verão apenas suas próprias avaliações. Administradores verão todas as avaliações.
- **Resposta de Sucesso**:
  - **Código**: 200 OK
  - **Conteúdo**: Lista de avaliações

### Obter detalhes de uma avaliação
- **URL**: `/pedidos/api/reviews/{id}/`
- **Método**: GET
- **Resposta de Sucesso**:
  - **Código**: 200 OK
  - **Conteúdo**: Detalhes da avaliação

### Criar uma nova avaliação
- **URL**: `/pedidos/api/reviews/`
- **Método**: POST
- **Dados**:
  ```json
  {
    "product": 1,
    "rating": 5,
    "comment": "Excelente produto!"
  }
  ```
- **Observação**: O usuário é automaticamente associado à avaliação.
- **Resposta de Sucesso**:
  - **Código**: 201 Created
  - **Conteúdo**: Detalhes da avaliação criada

### Atualizar uma avaliação
- **URL**: `/pedidos/api/reviews/{id}/`
- **Método**: PUT
- **Dados**:
  ```json
  {
    "product": 1,
    "rating": 4,
    "comment": "Muito bom, mas poderia ser melhor."
  }
  ```
- **Resposta de Sucesso**:
  - **Código**: 200 OK
  - **Conteúdo**: Detalhes da avaliação atualizada

### Atualizar parcialmente uma avaliação
- **URL**: `/pedidos/api/reviews/{id}/`
- **Método**: PATCH
- **Dados**:
  ```json
  {
    "rating": 3
  }
  ```
- **Resposta de Sucesso**:
  - **Código**: 200 OK
  - **Conteúdo**: Detalhes da avaliação atualizada

### Excluir uma avaliação
- **URL**: `/pedidos/api/reviews/{id}/`
- **Método**: DELETE
- **Resposta de Sucesso**:
  - **Código**: 204 No Content

## Painel Administrativo

Além da API REST, o sistema também oferece um painel administrativo completo acessível em:

- **URL**: `/admin/`

No painel administrativo, os administradores podem gerenciar todos os modelos do sistema (Produtos, Pedidos, Itens de Pedido e Avaliações) através de uma interface gráfica amigável.