from collections.abc import AsyncIterator, Sequence
from http import HTTPStatus
from typing import TypedDict

import aiohttp
import pytest
from aiocache import BaseCache
from aiohttp.web import Request, Response
from asyncly.srvmocker import JsonResponse, MockRoute, MockService, start_service
from asyncly.srvmocker.models import BaseMockResponse
from yarl import URL

from library.adapters.open_library.cached import CachedOpenLibraryClient
from library.adapters.open_library.client import OpenLibraryClient
from library.adapters.open_library.config import OpenLibraryConfig
from library.adapters.open_library.reduced import ReducedOpenLibraryClient
from library.domains.interfaces.clients.open_library import IOpenLibraryClient


@pytest.fixture()
async def open_library_service() -> AsyncIterator[MockService]:
    routes = [
        MockRoute("GET", "/search.json", "search"),
    ]
    async with start_service(routes=routes) as service:
        yield service


@pytest.fixture
def open_library_url(open_library_service: MockService) -> URL:
    return open_library_service.url


@pytest.fixture
def open_library_config(open_library_url: URL) -> OpenLibraryConfig:
    return OpenLibraryConfig(url=str(open_library_url))


@pytest.fixture
async def open_library_client(
    open_library_url: URL,
) -> AsyncIterator[OpenLibraryClient]:
    async with aiohttp.ClientSession() as session:
        yield OpenLibraryClient(
            url=open_library_url,
            session=session,
            client_name="test_open_library",
        )


@pytest.fixture
def cached_open_library_client(
    open_library_client: OpenLibraryClient,
    redis_cache: BaseCache,
) -> IOpenLibraryClient:
    return CachedOpenLibraryClient(
        client=open_library_client,
        cache=redis_cache,
    )


@pytest.fixture
def reduced_open_library_client(
    open_library_client: OpenLibraryClient,
) -> IOpenLibraryClient:
    return ReducedOpenLibraryClient(client=open_library_client)


class OpenLibraryDocDict(TypedDict):
    key: str
    title: str
    author_name: list[str]


class OpenLibrarySearchDict(TypedDict):
    num_found: int
    start: int
    offset: int
    docs: Sequence[OpenLibraryDocDict]


class OpenLibrarySearchResponse(BaseMockResponse):
    def __init__(self, books: Sequence[OpenLibraryDocDict]) -> None:
        self.books = books

    async def response(self, request: Request) -> Response:
        limit = int(request.query.get("limit", 20))
        offset = int(request.query.get("offset", 0))
        response = JsonResponse(
            body=OpenLibrarySearchDict(
                num_found=len(self.books),
                start=offset,
                offset=offset,
                docs=self.books[offset : offset + limit],
            ),
            status=HTTPStatus.OK,
        )
        return await response.response(request=request)
