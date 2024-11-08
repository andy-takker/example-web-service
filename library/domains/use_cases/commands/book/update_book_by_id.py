from dataclasses import dataclass

from library.application.use_case import ICommand
from library.domains.entities.book import Book, UpdateBook
from library.domains.services.book import BookService


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateBookByIdCommand(ICommand[UpdateBook, Book]):
    book_service: BookService

    async def execute(self, *, input_dto: UpdateBook) -> Book:
        return await self.book_service.update_book_by_id(update_book=input_dto)
