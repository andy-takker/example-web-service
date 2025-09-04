from library.application.reduced import AsyncReducer, IReduced, reduced
from library.domains.entities.open_library import OpenLibrarySearchResult
from library.domains.interfaces.clients.open_library import IOpenLibraryClient


class ReducedOpenLibraryClient(IReduced):
    def __init__(self, client: IOpenLibraryClient):
        self._client = client
        self._reducer = AsyncReducer()

    @reduced()
    async def search(
        self, query: str, limit: int, offset: int
    ) -> OpenLibrarySearchResult:
        return await self._client.search(query=query, limit=limit, offset=offset)
