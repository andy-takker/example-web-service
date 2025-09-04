from asyncly.srvmocker import MockService

from library.adapters.open_library.client import OpenLibraryClient
from library.domains.entities.open_library import (
    OpenLibraryBook,
    OpenLibrarySearchResult,
)
from tests.plugins.instances.open_library import OpenLibrarySearchResponse


async def test_open_library_client_search__empty(
    open_library_service: MockService,
    open_library_client: OpenLibraryClient,
):
    open_library_service.register("search", OpenLibrarySearchResponse(books=[]))

    result = await open_library_client.search(query="test", limit=10, offset=0)
    assert result == OpenLibrarySearchResult(
        books=[],
        total=0,
        start=0,
        offset=0,
    )


async def test_open_library_client_search__ok(
    open_library_service: MockService,
    open_library_client: OpenLibraryClient,
):
    open_library_service.register(
        "search",
        OpenLibrarySearchResponse(
            books=[
                {
                    "author_name": ["Test author"],
                    "title": "Test title",
                    "key": "test",
                }
            ]
        ),
    )

    result = await open_library_client.search(query="test", limit=10, offset=0)
    assert result == OpenLibrarySearchResult(
        books=[
            OpenLibraryBook(
                key="test",
                title="Test title",
                authors=["Test author"],
            )
        ],
        total=1,
        start=0,
        offset=0,
    )
