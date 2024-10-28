from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from library.domains.entities.book import Book, BookId, BookPaginationParams


class IBookStorage(Protocol):
    @abstractmethod
    async def fetch_book_by_id(self, *, book_id: BookId) -> Book | None:
        raise NotImplementedError

    @abstractmethod
    async def count_books(self, *, params: BookPaginationParams) -> int:
        raise NotImplementedError

    @abstractmethod
    async def fetch_book_list(self, *, params: BookPaginationParams) -> Sequence[Book]:
        raise NotImplementedError
