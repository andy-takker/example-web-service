from library.application.use_case import IUseCase
from library.domains.entities.book import Book, BookId
from library.domains.services.book import BookService


class FetchBookById(IUseCase[BookId, Book]):
    __book_service: BookService

    def __init__(self, book_service: BookService) -> None:
        self.__book_service = book_service

    async def execute(self, *, input_dto: BookId) -> Book:
        return await self.__book_service.fetch_book_by_id(book_id=input_dto)
