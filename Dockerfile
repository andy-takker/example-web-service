
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

RUN pip install -U pip uv
COPY pyproject.toml uv.lock /app/
RUN uv sync --no-dev --locked

USER appuser

ARG PROJECT_NAME=library

COPY ./${PROJECT_NAME} ./${PROJECT_NAME}

EXPOSE 8080
