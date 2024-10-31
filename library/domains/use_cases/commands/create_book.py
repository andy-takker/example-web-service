from library.application.use_case import ICommand
from library.domains.entities.book import Book, CreateBook
from library.domains.services.book import BookService


class CreateBookCommand(ICommand[CreateBook, Book]):
    def __init__(self, book_service: BookService) -> None:
        self.book_service = book_service

    async def execute(self, *, input_dto: CreateBook) -> Book:
        return await self.book_service.create_book(book=input_dto)
