from library.application.use_case import ICommand
from library.domains.entities.book import Book, CreateBook
from library.domains.services.book import BookService
from library.domains.uow import AbstractUow


class CreateBookCommand(ICommand[CreateBook, Book]):
    _uow: AbstractUow
    _book_service: BookService

    def __init__(
        self,
        *,
        uow: AbstractUow,
        book_service: BookService,
    ) -> None:
        self._uow = uow
        self._book_service = book_service

    async def execute(self, *, input_dto: CreateBook) -> Book:
        async with self._uow:
            return await self._book_service.create_book(book=input_dto)
