from http import HTTPStatus
from types import MappingProxyType

from asyncly import BaseHttpClient, ResponseHandlersType
from asyncly.client.handlers.msgspec import parse_struct

from library.adapters.open_library.schemas.search import OpenLibrarySearchStruct
from library.domains.entities.open_library import (
    OpenLibraryBook,
    OpenLibrarySearchResult,
)


class OpenLibraryClient(BaseHttpClient):
    SEARCH_HANLDERS: ResponseHandlersType = MappingProxyType(
        {HTTPStatus.OK: parse_struct(OpenLibrarySearchStruct)}
    )

    async def search(
        self, query: str, limit: int, offset: int
    ) -> OpenLibrarySearchResult:
        result: OpenLibrarySearchStruct = await self._make_req(
            method="GET",
            handlers=self.SEARCH_HANLDERS,
            url=self._url / "search.json",
            params={
                "q": query,
                "limit": limit,
                "offset": offset,
                "fields": ",".join(["key", "title", "author_name", "editions"]),
            },
        )
        return OpenLibrarySearchResult(
            books=[
                OpenLibraryBook(
                    key=book.key,
                    title=book.title,
                    authors=book.author_name,
                )
                for book in result.docs
                if book.author_name is not None
            ],
            total=result.num_found,
            start=result.start,
            offset=result.offset,
        )
