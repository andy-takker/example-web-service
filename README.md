# Example Web Service

Example web service for an internet library, built as a reference for clean,
layered Python services with both a REST API and async messaging in a single app.

## Features

- Layered architecture (`domain` / `adapters` / `presentors` / `application`)
  with import boundaries enforced by [import-linter](https://github.com/seddonym/import-linter)
- Dependency Injection with [dishka](https://github.com/reagento/dishka)
- REST API based on [litestar](https://github.com/litestar-org/litestar)
- Async pub/sub messaging with [faststream](https://github.com/ag2ai/faststream)
  over NATS JetStream
- External API integration ([Open Library](https://openlibrary.org/)) with
  caching and response reduction via [asyncly](https://github.com/andy-takker/asyncly)
- Database layer with [SQLAlchemy](https://www.sqlalchemy.org/) + asyncpg,
  the Unit of Work pattern, and Alembic migrations
- Redis for caching
- Observability: Prometheus metrics, structured logging with
  [structlog](https://www.structlog.org/), and optional
  [Sentry](https://sentry.io/) integration
- Rate limiting and CORS out of the box
- Auto tests with [pytest](https://docs.pytest.org/en/stable/) — unit tests on
  fakes plus integration tests against containerized services and external APIs
- Formatting and linting with [ruff](https://github.com/astral-sh/ruff) and
  [mypy](https://github.com/python/mypy)
- Dockerfile with best practices
- CI/CD with GitHub Workflows split into separate actions
- [pre-commit](https://github.com/pre-commit/pre-commit) hooks

## Working with the repo

### How to install dependencies?

Create a new venv in the project folder and install all dependencies with
[uv](https://github.com/astral-sh/uv):

```bash
make develop
```

### How to run dev containers for testing?

Start the Postgres, Redis, and NATS containers described in
`docker-compose.dev.yaml` from scratch:

```bash
make local
```

Stop them and drop the volumes:

```bash
make local-down
```

### How to run the service?

```bash
python -m library
```

The API is served on `http://127.0.0.1:8000` (see `.env` for host/port).
OpenAPI docs are available at `/docs/swagger` and `/docs/redoc`, Prometheus
metrics at `/metrics`.

### How to run tests?

Run the tests after dependencies are installed and while `make local` is running
in a separate terminal:

```bash
pytest -vx ./tests
```

### How to apply all actual migrations?

Remember that to connect to the database you must set the environment variables
`APP_DATABASE_HOST`, `APP_DATABASE_PORT`, `APP_DATABASE_USER`,
`APP_DATABASE_PASSWORD`, `APP_DATABASE_NAME`.

```bash
python -m library.adapters.database upgrade head
```

### How to generate a new migration?

Apply the existing migrations with the command above first.

```bash
python -m library.adapters.database revision --autogenerate -m "Your message"
```

### How to check import boundaries?

import-linter enforces the architectural layering (the domain must not import
adapters or presentors; adapters must not import presentors; production code must
not import tests):

```bash
make import-linter
```

### How to work with the repo in CI?

Separate commands are written in the `Makefile` to run dependency installation,
checks, and testing. They have the `-ci` suffix:

```bash
make develop-ci  # install dependencies
make lint-ci     # run linters - ruff, mypy and import-linter
make test-ci     # run tests with pytest and coverage
```

## Routes

### Books

```api
GET     /api/v1/books/            Fetch Books
POST    /api/v1/books/            Create Book
GET     /api/v1/books/{book_id}/  Fetch Book by ID
PATCH   /api/v1/books/{book_id}/  Update Book by ID
DELETE  /api/v1/books/{book_id}/  Delete Book by ID
```

### Users

```api
GET     /api/v1/users/             Fetch Users
POST    /api/v1/users/             Create User
GET     /api/v1/users/{user_id}/   Fetch User by ID
PATCH   /api/v1/users/{user_id}/   Update User by ID
DELETE  /api/v1/users/{user_id}/   Delete User by ID
```

### Open Library

```api
GET     /api/v1/open-library/search   Search books in Open Library
```
</content>
</invoke>
