# Teste da TMJ
Esta é uma API RESTful simples para gerenciar tarefas.
## O projeto é construído com:

- Django;
- Django REST Framework;
- SQLite (banco de dados padrão conforme pedido);
- djangorestframework-simplejwt para autenticação.

## Requisitos
Para rodar o projeto, você precisa ter o Docker e o Docker Compose instalados na sua máquina.

## Como Rodar o Projeto
Execute no terminal da sua máquina no diretório que escolher:

```bash
git clone https://github.com/rpablogomes/tmj-django
cd tmj-django
docker-compose up --build
```


O servidor estará disponível em:
http://127.0.0.1:8000

## Rotas da API
### Autenticação via JWT

- **POST** `http://localhost:8000/api/register/` → Autentica um usuário e retorna os tokens de acesso e refresh.
```bash
  {
    "username": "usuario",
    "password": "senha"
  }
```
- **POST** `http://127.0.0.1:8000/api/token/` → Autentica um usuário e retorna os tokens de acesso e refresh.
```bash
  {
    "username": "usuario",
    "password": "senha"
  }
```
- **POST** `http://127.0.0.1:8000/api/token/refresh/` → Renova o token de acesso usando um token de refresh.
```bash
{
"refresh": "refresh token"
}
```
- **POST** `http://127.0.0.1:8000/api/token/blacklist/` → Adiciona um token de refresh à blacklist (logout).
```bash
{
"refresh": "refresh token"
}
```

Todas as rotas de tarefas exigem um token de acesso válido no cabeçalho:

**Authorization**: Bearer <seu_token>

### Endpoints para Tarefas

- **GET** `http://127.0.0.1:8000/api/tarefas` → Lista todas as tarefas do usuário autenticado.
- **POST** `http://127.0.0.1:8000/api/tarefas` → Cria uma nova tarefa.
- **GET** `http://127.0.0.1:8000/api/tarefas/<id>` → Retorna os detalhes de uma tarefa específica.
- **PUT** `http://127.0.0.1:8000/api/tarefas/<id>` → Atualiza todos os campos de uma tarefa.
- **PATCH** `http://127.0.0.1:8000/api/tarefas/<id>` → Atualiza parcialmente os campos de uma tarefa.
- **DELETE** `http://127.0.0.1:8000/api/tarefas/<id>` → Deleta uma tarefa específica.

### Filtros de Tarefas
#### Listar apenas tarefas concluídas
- **GET** `http://127.0.0.1:8000/api/tarefas?completed=true`

#### Listar apenas tarefas não concluídas
- **GET** `http://127.0.0.1:8000/api/tarefas?completed=false`
