from library.application.exceptions import EntityNotFoundException
from library.domains.entities.book import (
    Book,
    BookId,
    BookPagination,
    BookPaginationParams,
)
from library.domains.interfaces.storages.book import IBookStorage


class BookService:
    __book_storage: IBookStorage

    def __init__(self, book_storage: IBookStorage) -> None:
        self.__book_storage = book_storage

    async def fetch_book_by_id(self, *, book_id: BookId) -> Book:
        book = await self.__book_storage.fetch_book_by_id(book_id=book_id)
        if book is None:
            raise EntityNotFoundException(entity=Book, entity_id=book_id)
        return book

    async def fetch_book_list(self, *, params: BookPaginationParams) -> BookPagination:
        total = await self.__book_storage.count_books(params=params)
        items = await self.__book_storage.fetch_book_list(params=params)
        return BookPagination(total=total, items=items)
