# Example Web Service

Example REST web service for internet library with:

- clean architecture with interfaces, layers and entities
- Dependency Injection with [dishka](https://github.com/reagento/dishka)
- auto tests with [pytest](https://docs.pytest.org/en/stable/)
- formatting and linting with [ruff](https://github.com/astral-sh/ruff) and [mypy](https://github.com/python/mypy)
- Dockerfile with best practices
- CI/CD with Github Workflows with separated actions
- [pre-commit](https://github.com/pre-commit/pre-commit) features

## Working with repos

### How to install dependencies?

Creating new venv in project folder and install all dependencies with poetry:

```bash
make develop
```

### How to run dev containers for testing?

Start postgres container described in `docker-compose.dev.yaml` from scratch:

```bash
make local
```

### How to run tests?

The tests must be run after the dependencies are installed and when the `make local` process is running separately:

```bash
pytest -vx ./tests
```

### How to apply all actual migrations?

Remember that to connect to the database, you must specify the environment
variable `APP_DATABASE_DSN`

```bash
python -m library.adapters.database upgrade head
```

### How to generate new migration?

Don't forget to apply migrations with the above command first.

```bash
python -m library.adapters.database revision --autogenerate -m "Your message"
```

### How to work with repo in CI?

Separate commands are written in the `Makefile` to run dependency
installation, checks, and testing. They have the suffix `-ci`

```bash
make develop-ci  # install dependencies
make lint-ci     # run linters - ruff and mypy
make test-ci     # run tests with pytest and coverage
```

## Routes

List of routes:

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
POST    /api/v1/users/             Create Book
GET     /api/v1/users/{user_id}/   Fetch User by ID
PATCH   /api/v1/users/{user_id}/   Update User by ID
DELETE  /api/v1/users/{user_id}/   Delete User by ID
```

### User Books

```api
GET     /api/v1/users/{user_id}/books/                   Get user books
POST    /api/v1/users/{user_id}/books/{book_id}/issue/   Issue Book to User
POST    /api/v1/users/{user_id}/books/{book_id}/return/  Return Book from User
```
