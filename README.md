# Guia de execução

## Pré-requisitos

- Docker instalado e rodando
- Docker Compose plugin (`docker compose`)

---

## Configurar o arquivo .env

Crie o arquivo dotenv_files/.env

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
---

## Subir o projeto pela primeira vez 

```bash
docker compose up --build
```

- Builda a imagem do Django
- Sobe os containers (app + banco)
- Aguarda o Postgres iniciar
- Roda `collectstatic`, `makemigrations` e `migrate` automaticamente
- Inicia o servidor em `http://localhost:8000`

---

## Das próximas vezes

```bash
docker compose up
```

---

## Parar os containers

```bash
docker compose down
```

---

## Rebuild

Rebuild é necessário quando ao alterar dockerfile, app/requirements.txt ou scripts/commands.sh




