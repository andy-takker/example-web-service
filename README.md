<div align="center">

# 📚 Example Web Service

*Async Python service — **Litestar** + **FastStream/NATS**, clean layered architecture, DI and import-linter*

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![CI](https://github.com/andy-takker/example-web-service/actions/workflows/feature.yaml/badge.svg)](https://github.com/andy-takker/example-web-service/actions/workflows/feature.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

[![Litestar](https://img.shields.io/badge/Litestar-2.x-edb641?logo=litestar&logoColor=white)](https://litestar.dev/)
[![FastStream](https://img.shields.io/badge/FastStream-0.5-009485?logo=apachekafka&logoColor=white)](https://faststream.ag2.ai/)
[![NATS](https://img.shields.io/badge/NATS-JetStream-27AAE1?logo=natsdotio&logoColor=white)](https://nats.io/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Redis](https://img.shields.io/badge/Redis-cache-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![dishka](https://img.shields.io/badge/DI-dishka-4B8BBE)](https://github.com/reagento/dishka)

[![uv](https://img.shields.io/badge/uv-managed-DE5FE9?logo=uv&logoColor=white)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/badge/lint-ruff-D7FF64?logo=ruff&logoColor=black)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/typing-mypy-2A6DB2)](https://www.mypy-lang.org/)
[![import-linter](https://img.shields.io/badge/architecture-import--linter-1f6feb)](https://github.com/seddonym/import-linter)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-FAB040?logo=precommit&logoColor=black)](https://github.com/pre-commit/pre-commit)

</div>

---

Example web service for an internet library, built as a reference for clean,
layered Python services with both a REST API and async messaging in a single app.

## ✨ Features

- 🧱 **Layered architecture** (`domain` / `adapters` / `presentors` / `application`)
  with import boundaries enforced by [import-linter](https://github.com/seddonym/import-linter)
- 💉 **Dependency Injection** with [dishka](https://github.com/reagento/dishka)
- 🌐 **REST API** based on [Litestar](https://litestar.dev/)
- 📨 **Async pub/sub messaging** with [FastStream](https://faststream.ag2.ai/)
  over NATS JetStream
- 🔌 **External API integration** ([Open Library](https://openlibrary.org/)) with
  caching and response reduction via [asyncly](https://github.com/andy-takker/asyncly)
- 🗄️ **Database layer** with [SQLAlchemy](https://www.sqlalchemy.org/) + asyncpg,
  the Unit of Work pattern, and [Alembic](https://alembic.sqlalchemy.org/) migrations
- ⚡ **Redis** for caching
- 📊 **Observability**: Prometheus metrics, structured logging with
  [structlog](https://www.structlog.org/), and optional [Sentry](https://sentry.io/)
- 🛡️ **Rate limiting** and **CORS** out of the box
- 🧪 **Auto tests** with [pytest](https://docs.pytest.org/en/stable/) — unit tests on
  fakes plus integration tests against containerized services and external APIs
- 🎨 **Formatting & linting** with [Ruff](https://github.com/astral-sh/ruff) and
  [mypy](https://github.com/python/mypy)
- 🐳 **Dockerfile** with best practices
- 🔁 **CI/CD** with GitHub Workflows split into separate actions
- ✅ [pre-commit](https://github.com/pre-commit/pre-commit) hooks

## 🏗️ Architecture

The codebase is split into layers with one-way dependencies, verified on every
commit by import-linter:

```
presentors  →  application  →  adapters  →  domain
   (REST / FastStream)          (db, redis, nats, open_library)
```

Enforced contracts:

- `domain` must not import `adapters` or `presentors`
- `adapters` must not import `presentors`
- production code must not import `tests`

## 🚀 Getting started

### Install dependencies

Create a venv in the project folder and install everything with
[uv](https://github.com/astral-sh/uv):

```bash
make develop
```

### Run dev containers

Start the Postgres, Redis, and NATS containers from `docker-compose.dev.yaml`:

```bash
make local       # start
make local-down  # stop and drop volumes
```

### Run the service

```bash
python -m library
```

The API is served on `http://127.0.0.1:8000` (see `.env` for host/port):

| Endpoint           | Description           |
| ------------------ | --------------------- |
| `/docs/swagger`    | Swagger UI            |
| `/docs/redoc`      | ReDoc                 |
| `/metrics`         | Prometheus metrics    |

### Run tests

Run after dependencies are installed and while `make local` is running in a
separate terminal:

```bash
pytest -vx ./tests
```

## 🗃️ Database migrations

To connect to the database, set the env variables `APP_DATABASE_HOST`,
`APP_DATABASE_PORT`, `APP_DATABASE_USER`, `APP_DATABASE_PASSWORD`,
`APP_DATABASE_NAME`.

```bash
# apply all migrations
python -m library.adapters.database upgrade head

# generate a new migration (apply existing ones first)
python -m library.adapters.database revision --autogenerate -m "Your message"
```

## 🤖 Working in CI

Separate `Makefile` targets (suffixed `-ci`) install dependencies, run checks,
and run tests:

```bash
make develop-ci  # install dependencies
make lint-ci     # run linters - ruff, mypy and import-linter
make test-ci     # run tests with pytest and coverage
```

Check import boundaries on their own:

```bash
make import-linter
```

## 🗺️ Routes

### 📖 Books

```api
GET     /api/v1/books/            Fetch Books
POST    /api/v1/books/            Create Book
GET     /api/v1/books/{book_id}/  Fetch Book by ID
PATCH   /api/v1/books/{book_id}/  Update Book by ID
DELETE  /api/v1/books/{book_id}/  Delete Book by ID
```

### 👤 Users

```api
GET     /api/v1/users/             Fetch Users
POST    /api/v1/users/             Create User
GET     /api/v1/users/{user_id}/   Fetch User by ID
PATCH   /api/v1/users/{user_id}/   Update User by ID
DELETE  /api/v1/users/{user_id}/   Delete User by ID
```

### 🔍 Open Library

```api
GET     /api/v1/open-library/search   Search books in Open Library
```

## 📄 License

Released under the [MIT License](./LICENSE).
