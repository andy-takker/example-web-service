from library.application.use_case import ICommand
from library.domains.entities.book import Book, UpdateBook
from library.domains.services.book import BookService
from library.domains.uow import AbstractUow


class UpdateBookByIdCommand(ICommand[UpdateBook, Book]):
    _uow: AbstractUow
    _book_service: BookService

    def __init__(self, *, uow: AbstractUow, book_service: BookService) -> None:
        self._uow = uow
        self._book_service = book_service

    async def execute(self, *, input_dto: UpdateBook) -> Book:
        async with self._uow:
            return await self._book_service.update_book_by_id(update_book=input_dto)
