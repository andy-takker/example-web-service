from collections.abc import AsyncIterator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from library.adapters.database.config import DatabaseConfig
from library.adapters.nats.config import NatsConfig
from library.adapters.open_library.config import OpenLibraryConfig
from library.adapters.redis.config import RedisConfig
from library.application.config import AppConfig
from library.config import Config
from library.presentors.rest.service import get_fastapi_app


@pytest.fixture
def config(
    db_config: DatabaseConfig,
    redis_config: RedisConfig,
    open_library_config: OpenLibraryConfig,
    nats_config: NatsConfig,
) -> Config:
    return Config(
        app=AppConfig(debug=True),
        database=db_config,
        redis=redis_config,
        open_library=open_library_config,
        nats=nats_config,
    )


@pytest.fixture
def fastapi_app(config: Config) -> FastAPI:
    return get_fastapi_app(config=config)


@pytest.fixture
async def client(
    fastapi_app: FastAPI, engine, clear_redis_cache
) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app),
        base_url="http://testserver",
    ) as client:
        yield client
