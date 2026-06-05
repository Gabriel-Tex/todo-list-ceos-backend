# Todo List — Backend

API REST para gerenciamento de tarefas (TODO list) com autenticação JWT. Desenvolvida com Django e Django REST Framework, conteinerizada com Docker e PostgreSQL.

---

## Sumário

- [Stack](#stack)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Modelo de dados](#modelo-de-dados)
- [Endpoints da API](#endpoints-da-api)
  - [Autenticação](#autenticação)
  - [Tarefas](#tarefas)
- [Autenticação JWT](#autenticação-jwt)
- [Query params disponíveis](#query-params-disponíveis)
- [Como executar](#como-executar)
- [Variáveis de ambiente](#variáveis-de-ambiente)

---

## Stack

* Python 
* Django 
* Django REST Framework 
* SimpleJWT 
* PostgreSQL 
* Docker + Docker Compose 

---

## Estrutura do projeto

```
todo-list-ceos/
├── app/
│   ├── authentication/          # Módulo de autenticação
│   │   ├── migrations/
│   │   ├── serializers.py       # Serializers de User (registro e perfil)
│   │   ├── views.py             # Register, Profile
│   │   └── urls.py              # Rotas de autenticação
│   ├── tasks/                   # Módulo de tarefas
│   │   ├── migrations/
│   │   ├── models.py            # Modelo Task
│   │   ├── serializers.py       # Serializer de Task
│   │   ├── views.py             # CRUD + busca/filtros
│   │   └── urls.py              # Rotas de tarefas
│   ├── project/
│   │   ├── settings.py          # Configurações do Django
│   │   └── urls.py              # Roteamento central
│   ├── manage.py
│   └── requirements.txt
├── scripts/
│   └── commands.sh              # Entrypoint do container
├── dotenv_files/
│   ├── .env                     # Variáveis de ambiente (não versionar)
│   └── .env-example             # Modelo para criação do .env
├── Dockerfile
└── docker-compose.yml
```

A aplicação segue **arquitetura modular**: cada funcionalidade (autenticação, tarefas) é isolada em seu próprio app Django, com seus próprios models, serializers, views e urls.

---

## Modelo de dados

### Task

Representa uma tarefa do usuário.

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|---|---|---|---|---|
| `id` | integer | — | auto | Chave primária |
| `title` | string (100) | ✅ | — | Título da tarefa |
| `description` | text | ❌ | `""` | Descrição detalhada |
| `priority` | string (enum) | ❌ | `"medium"` | Prioridade: `low`, `medium`, `high` |
| `status` | string (enum) | ❌ | `"pending"` | Estado: `pending`, `completed` |
| `final_date` | date | ❌ | `null` | Prazo (formato `YYYY-MM-DD`) |
| `created_at` | datetime | — | auto | Data de criação (somente leitura) |
| `owner` | integer (FK) | — | auto | ID do usuário dono (somente leitura) |

O campo `owner` é sempre definido automaticamente pelo backend com base no usuário autenticado — o cliente nunca precisa (nem deve) enviá-lo.

---

## Endpoints da API

Base URL: `http://localhost:8000`

Todos os endpoints de tarefas exigem o header de autorização:

```
Authorization: Bearer <access_token>
```

### Autenticação

#### `POST /api/register/`

Cria um novo usuário. Retorna os dados do usuário e os tokens JWT, dispensando um login separado após o cadastro.

**Request body:**
```json
{
  "username": "dionisio",
  "email": "dionisio@email.com",
  "password": "naoseiasenha123"
}
```

**Response `201 Created`:**
```json
{
  "user": {
    "id": 1,
    "username": "dionisio",
    "email": "dionisio@email.com",
    "date_joined": "2026-06-04T21:00:00Z"
  },
  "tokens": {
    "refresh": "<refresh_token>",
    "access": "<access_token>"
  }
}
```

---

#### `POST /api/login/`

Autentica um usuário existente e retorna o par de tokens JWT.

**Request body:**
```json
{
  "username": "dionisio",
  "password": "naoseiasenha123"
}
```

**Response `200 OK`:**
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

---

#### `POST /api/logout/`

Invalida o refresh token (adiciona à blacklist), efetivando o logout.

**Request body:**
```json
{
  "refresh": "<refresh_token>"
}
```

**Response `200 OK`:** corpo vazio.

---

#### `GET /api/profile/`

Retorna os dados do usuário autenticado. Requer o header `Authorization`.

**Response `200 OK`:**
```json
{
  "id": 1,
  "username": "dionisio",
  "email": "dionisio@email.com",
  "date_joined": "2026-06-04T21:00:00Z"
}
```

---

### Tarefas

Todos os endpoints abaixo exigem `Authorization: Bearer <access_token>`. Cada usuário só pode visualizar e manipular as próprias tarefas.

---

#### `GET /api/tasks/`

Lista todas as tarefas do usuário autenticado, ordenadas da mais recente para a mais antiga.

Aceita [query params](#query-params-disponíveis) para busca e filtragem.

**Response `200 OK`:**
```json
[
  {
    "id": 1,
    "title": "Fazer compras",
    "description": "Mercado e farmácia",
    "priority": "high",
    "status": "pending",
    "owner": 1,
    "final_date": "2026-06-10",
    "created_at": "2026-06-04T21:30:00Z"
  }
]
```

---

#### `POST /api/tasks/`

Cria uma nova tarefa para o usuário autenticado.

**Request body:**
```json
{
  "title": "Fazer compras",
  "description": "Mercado e farmácia",
  "priority": "high",
  "final_date": "2026-06-10"
}
```

Apenas `title` é obrigatório. Os campos `status`, `priority` e `description` têm valores padrão e podem ser omitidos.

**Response `201 Created`:** objeto da tarefa criada (mesmo formato do GET).

---

#### `GET /api/tasks/<id>/`

Retorna o detalhe de uma tarefa específica pelo seu `id`.

**Response `200 OK`:** objeto da tarefa.

**Response `404 Not Found`:** se a tarefa não existir ou não pertencer ao usuário autenticado.

---

#### `PUT /api/tasks/<id>/`

Atualiza todos os campos de uma tarefa. Todos os campos editáveis devem ser enviados.

**Request body:**
```json
{
  "title": "Fazer compras",
  "description": "Só o mercado",
  "priority": "medium",
  "status": "completed",
  "final_date": "2026-06-10"
}
```

**Response `200 OK`:** objeto da tarefa atualizada.

---

#### `PATCH /api/tasks/<id>/`

Atualiza parcialmente uma tarefa. Ideal para marcar como concluída sem reenviar todos os campos.

**Exemplo — marcar como concluída:**
```json
{
  "status": "completed"
}
```

**Response `200 OK`:** objeto da tarefa atualizada.

---

#### `DELETE /api/tasks/<id>/`

Remove permanentemente uma tarefa.

**Response `204 No Content`.**

---

## Autenticação JWT

O sistema usa JSON Web Tokens com dois tipos de token:

**Access token** — usado nas requisições como `Authorization: Bearer <token>`. Tem vida curta (30 minutos) por segurança. Quando expirar, o frontend deve obter um novo usando o refresh token, sem exigir novo login do usuário.

**Refresh token** — válido por 7 dias. Usado exclusivamente para renovar o access token.

O logout funciona adicionando o refresh token à **blacklist**, impedindo sua reutilização mesmo antes de expirar. O access token não é invalidado explicitamente — ele simplesmente expira dentro de sua janela de validade.

Configurações ativas (`settings.py`):

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

---

## Query params disponíveis

O endpoint `GET /api/tasks/` aceita os parâmetros abaixo na query string para filtrar e ordenar resultados.

### Busca por título

```
GET /api/tasks/?search=compras
```

Retorna todas as tarefas cujo título contenha o termo buscado (case-insensitive).

### Filtro por status

```
GET /api/tasks/?status=pending
GET /api/tasks/?status=completed
```

### Filtro por prioridade

```
GET /api/tasks/?priority=low
GET /api/tasks/?priority=medium
GET /api/tasks/?priority=high
```

### Ordenação

```
GET /api/tasks/?ordering=final_date
GET /api/tasks/?ordering=-final_date   (decrescente)
GET /api/tasks/?ordering=priority
GET /api/tasks/?ordering=status
```

### Combinando parâmetros

Os parâmetros podem ser combinados livremente:

```
GET /api/tasks/?search=projeto&status=pending&ordering=-final_date
```

---

## Como executar

### Pré-requisitos

- Docker instalado e rodando
- Docker Compose plugin (`docker compose`)

### 1. Configurar o arquivo `.env`

Copie o arquivo de exemplo e edite com os seus valores:

```bash
cp dotenv_files/.env-example dotenv_files/.env
```

Edite `dotenv_files/.env`:

```env
SECRET_KEY="chave-secreta"
DEBUG="1"
ALLOWED_HOSTS="127.0.0.1, localhost"

DB_ENGINE="django.db.backends.postgresql"
POSTGRES_DB="nome-do-banco"
POSTGRES_USER="usuario"
POSTGRES_PASSWORD="senha-forte"
POSTGRES_HOST="psql"
POSTGRES_PORT="5432"
```

> `POSTGRES_HOST` deve ser `psql` — esse é o nome do serviço do banco dentro da rede Docker.

### 2. Subir o projeto pela primeira vez

```bash
docker compose up --build
```

Este comando:
- Builda a imagem do Django a partir do `Dockerfile`
- Sobe os dois containers: `app` (Django) e `psql` (PostgreSQL)
- Aguarda o PostgreSQL estar disponível antes de prosseguir
- Executa `collectstatic` e `migrate` automaticamente
- Inicia o servidor em `http://localhost:8000`

### Das próximas vezes

```bash
docker compose up
```

### Parar os containers

```bash
docker compose down
```

### Rebuild

Necessário ao alterar `Dockerfile`, `app/requirements.txt` ou `scripts/commands.sh`:

```bash
docker compose up --build
```
