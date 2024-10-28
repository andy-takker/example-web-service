
ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN pip install -U pip poetry && poetry config virtualenvs.create false

RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=poetry.lock,target=poetry.lock \
    poetry install --no-interaction --no-ansi --no-dev

USER appuser

ARG PROJECT_NAME=library

COPY ./${PROJECT_NAME} ./${PROJECT_NAME}

EXPOSE 8080
