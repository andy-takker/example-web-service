from dataclasses import dataclass

from library.application.use_case import ICommand
from library.domains.entities.book import Book, CreateBook
from library.domains.services.book import BookService


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateBookCommand(ICommand[CreateBook, Book]):
    book_service: BookService

    async def execute(self, *, input_dto: CreateBook) -> Book:
        return await self.book_service.create_book(book=input_dto)
