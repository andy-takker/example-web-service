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
    async def fetch_book_by_id(self, *, book_id: BookId) -> Book | None: ...

    async def count_books(self, *, params: BookPaginationParams) -> int: ...

    async def fetch_book_list(
        self, *, params: BookPaginationParams
    ) -> Sequence[Book]: ...

    async def create_book(self, *, book: CreateBook) -> Book: ...

    async def delete_book_by_id(self, *, book_id: BookId) -> None: ...

    async def update_book_by_id(self, *, update_book: UpdateBook) -> Book: ...

    async def exists_book_by_id(self, *, book_id: BookId) -> bool: ...

    async def save_bulk_books(self, *, books: Sequence[CreateBook]) -> None: ...
