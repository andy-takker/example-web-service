from asyncly.srvmocker import MockService

from library.adapters.open_library.cached import CachedOpenLibraryClient
from tests.plugins.instances.open_library import OpenLibrarySearchResponse


async def test_cached_open_library_client_search__cache_hit(
    open_library_service: MockService,
    cached_open_library_client: CachedOpenLibraryClient,
):
    open_library_service.register("search", OpenLibrarySearchResponse(books=[]))
    await cached_open_library_client.search(query="test", limit=10, offset=0)
    await cached_open_library_client.search(query="test", limit=10, offset=0)

    assert len(open_library_service.history_map["search"]) == 1


async def test_cached_open_library_client_search__cache_miss(
    open_library_service: MockService,
    cached_open_library_client: CachedOpenLibraryClient,
):
    open_library_service.register("search", OpenLibrarySearchResponse(books=[]))
    await cached_open_library_client.search(query="test1", limit=10, offset=0)
    await cached_open_library_client.search(query="test2", limit=10, offset=0)

    assert len(open_library_service.history_map["search"]) == 2
