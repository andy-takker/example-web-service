from http import HTTPStatus

from asyncly.srvmocker import MockService
from httpx import AsyncClient

from tests.plugins.instances.open_library import OpenLibrarySearchResponse

API_URL = "/api/v1/open-library/search"


async def test_open_library_search__ok__status_code(
    client: AsyncClient, open_library_service: MockService
):
    open_library_service.register(
        "search",
        OpenLibrarySearchResponse(
            books=[
                {
                    "key": "book_key",
                    "title": "Book Title",
                    "author_name": ["Test author"],
                }
            ]
        ),
    )

    response = await client.get(API_URL, params={"query": "test"})
    assert response.status_code == HTTPStatus.OK


async def test_open_library_search__ok__format(
    client: AsyncClient, open_library_service: MockService
):
    open_library_service.register(
        "search",
        OpenLibrarySearchResponse(
            books=[
                {
                    "key": "book_key",
                    "title": "Book Title",
                    "author_name": ["Test author"],
                }
            ]
        ),
    )

    response = await client.get(API_URL, params={"query": "test"})
    assert response.json() == {
        "total": 1,
        "start": 0,
        "offset": 0,
        "books": [
            {
                "key": "book_key",
                "title": "Book Title",
                "authors": ["Test author"],
            }
        ],
    }


async def test_open_library_search__ok__limit_offset(
    client: AsyncClient, open_library_service: MockService
):
    open_library_service.register(
        "search",
        OpenLibrarySearchResponse(
            books=[
                {
                    "key": "book_key1",
                    "title": "Book Title 1",
                    "author_name": ["Test author 1"],
                },
                {
                    "key": "book_key2",
                    "title": "Book Title 2",
                    "author_name": ["Test author 2"],
                },
                {
                    "key": "book_key3",
                    "title": "Book Title 3",
                    "author_name": ["Test author 3"],
                },
            ]
        ),
    )

    response = await client.get(
        API_URL, params={"query": "test", "limit": 1, "offset": 1}
    )
    assert response.json() == {
        "total": 3,
        "start": 1,
        "offset": 1,
        "books": [
            {
                "key": "book_key2",
                "title": "Book Title 2",
                "authors": ["Test author 2"],
            }
        ],
    }
