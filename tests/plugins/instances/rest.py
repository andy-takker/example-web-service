from collections.abc import AsyncIterator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from library.presentors.rest.config import RestConfig
from library.presentors.rest.service import RestService


@pytest.fixture
def app(rest_config: RestConfig) -> FastAPI:
    return RestService(config=rest_config).create_application()


@pytest.fixture
async def client(app: FastAPI, engine) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        yield client
