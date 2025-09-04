from library.application.use_case import IQuery
from library.domains.entities.open_library import (
    OpenLibrarySearchParams,
    OpenLibrarySearchResult,
)
from library.domains.interfaces.clients.open_library import IOpenLibraryClient


class OpenLibrarySearchQuery(IQuery[OpenLibrarySearchParams, OpenLibrarySearchResult]):
    def __init__(self, *, client: IOpenLibraryClient) -> None:
        self._client = client

    async def execute(
        self, *, input_dto: OpenLibrarySearchParams
    ) -> OpenLibrarySearchResult:
        result = await self._client.search(
            query=input_dto.query,
            limit=input_dto.limit,
            offset=input_dto.offset,
        )
        return result
