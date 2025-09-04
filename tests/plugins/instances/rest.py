from collections.abc import AsyncIterator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from library.adapters.database.config import DatabaseConfig
from library.adapters.open_library.config import OpenLibraryConfig
from library.adapters.redis.config import RedisConfig
from library.application.config import AppConfig
from library.presentors.rest.config import RestConfig
from library.presentors.rest.service import RestService


@pytest.fixture
def rest_config(
    db_config: DatabaseConfig,
    redis_config: RedisConfig,
    open_library_config: OpenLibraryConfig,
) -> RestConfig:
    return RestConfig(
        app=AppConfig(debug=True),
        database=db_config,
        redis=redis_config,
        open_library=open_library_config,
    )


@pytest.fixture
def app(rest_config: RestConfig) -> FastAPI:
    return RestService(config=rest_config).create_application()


@pytest.fixture
async def client(app: FastAPI, engine, clear_redis_cache) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        yield client
