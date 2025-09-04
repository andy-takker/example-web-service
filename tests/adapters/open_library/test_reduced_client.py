from asyncio import gather

from asyncly.srvmocker import MockService
from asyncly.srvmocker.responses import LatencyResponse

from library.adapters.open_library.cached import CachedOpenLibraryClient
from tests.plugins.instances.open_library import OpenLibrarySearchResponse


async def test_reduce_open_library_client_search__ok(
    open_library_service: MockService,
    reduced_open_library_client: CachedOpenLibraryClient,
):
    open_library_service.register(
        "search",
        LatencyResponse(
            wrapped=OpenLibrarySearchResponse(books=[]),
            latency=0.2,
        ),
    )
    await gather(
        reduced_open_library_client.search(query="test", limit=10, offset=0),
        reduced_open_library_client.search(query="test", limit=10, offset=0),
    )

    assert len(open_library_service.history_map["search"]) == 1
