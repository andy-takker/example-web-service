PROJECT_NAME = library
TEST_FOLDER_NAME = tests
PYTHON_VERSION = 3.12

develop: clean_dev ##@Develop Create virtualenv
	python$(PYTHON_VERSION) -m venv .venv
	.venv/bin/pip install -U pip uv
	.venv/bin/uv sync
	.venv/bin/pre-commit install

local: ##@Develop Run dev containers for test
	docker compose -f docker-compose.dev.yaml up --force-recreate --renew-anon-volumes --build

local-down: ##@Develop Stop dev containers with delete volumes
	docker compose -f docker-compose.dev.yaml down -v

develop-ci: ##@Develop Create virtualenv for CI
	python -m pip install -U pip uv
	uv sync --all-groups --all-extras

test-ci: ##@Test Run tests with pytest and coverage in CI
	.venv/bin/pytest ./$(TEST_FOLDER_NAME) --junitxml=./junit.xml --cov=./$(PROJECT_NAME) --cov-report=xml

lint-ci: ruff mypy ##@Linting Run all linters in CI

ruff: ##@Linting Run ruff
	.venv/bin/ruff check ./$(PROJECT_NAME)

mypy: ##@Linting Run mypy
	.venv/bin/mypy --config-file ./pyproject.toml ./$(PROJECT_NAME) --enable-incomplete-feature=NewGenericSyntax

alembic_init: ##@Database Run alembic init for async
	.venv/bin/alembic init -t async ./$(PROJECT_NAME)/adapters/database/migrations

clean_dev: ##@Develop Remove virtualenv
	rm -rf .venv

HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \

help: ##@Help Show this help
	@echo -e "Usage: make [target] ... \n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)
