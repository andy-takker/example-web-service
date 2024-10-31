from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from library.domains.entities.book import (
    Book,
    BookId,
    BookPaginationParams,
    CreateBook,
    UpdateBook,
)


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

    @abstractmethod
    async def create_book(self, *, book: CreateBook) -> Book:
        raise NotImplementedError

    @abstractmethod
    async def delete_book_by_id(self, *, book_id: BookId) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_book_by_id(self, *, update_book: UpdateBook) -> Book:
        raise NotImplementedError
