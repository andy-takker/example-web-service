from collections.abc import Sequence

from library.application.exceptions import EntityNotFoundException
from library.domains.entities.book import (
    Book,
    BookId,
    BookPagination,
    BookPaginationParams,
    CreateBook,
    UpdateBook,
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

    async def create_book(self, *, book: CreateBook) -> Book:
        return await self.__book_storage.create_book(book=book)

    async def delete_book_by_id(self, *, book_id: BookId) -> None:
        if not await self.__book_storage.exists_book_by_id(book_id=book_id):
            raise EntityNotFoundException(entity=Book, entity_id=book_id)
        await self.__book_storage.delete_book_by_id(book_id=book_id)

    async def update_book_by_id(self, *, update_book: UpdateBook) -> Book:
        if not await self.__book_storage.exists_book_by_id(book_id=update_book.id):
            raise EntityNotFoundException(entity=Book, entity_id=update_book.id)
        return await self.__book_storage.update_book_by_id(update_book=update_book)

    async def save_bulk_books(self, *, books: Sequence[CreateBook]) -> None:
        await self.__book_storage.save_bulk_books(books=books)
