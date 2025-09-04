from library.application.use_case import IQuery
from library.domains.entities.book import Book, BookId
from library.domains.services.book import BookService
from library.domains.uow import AbstractUow


class FetchBookByIdQuery(IQuery[BookId, Book]):
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

    async def execute(self, *, input_dto: BookId) -> Book:
        async with self._uow:
            return await self._book_service.fetch_book_by_id(book_id=input_dto)
