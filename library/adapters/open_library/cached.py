from aiocache import BaseCache

from library.application.cached import ICached, cached
from library.domains.entities.open_library import OpenLibrarySearchResult
from library.domains.interfaces.clients.open_library import IOpenLibraryClient


class CachedOpenLibraryClient(ICached):
    def __init__(self, client: IOpenLibraryClient, cache: BaseCache):
        self._client = client
        self._cache = cache

    @cached(ttl=60 * 60)
    async def search(
        self, query: str, limit: int, offset: int
    ) -> OpenLibrarySearchResult:
        return await self._client.search(query=query, limit=limit, offset=offset)
