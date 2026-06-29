from abc import abstractmethod
from typing import Protocol

from library.domain.entities.open_library import (
    OpenLibrarySearchResult,
)


class IOpenLibraryClient(Protocol):
    @abstractmethod
    async def search(
        self, query: str, limit: int, offset: int
    ) -> OpenLibrarySearchResult: ...
