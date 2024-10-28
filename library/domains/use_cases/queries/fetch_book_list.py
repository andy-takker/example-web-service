from library.application.use_case import IUseCase
from library.domains.entities.book import BookPagination, BookPaginationParams
from library.domains.services.book import BookService


class FetchBookList(IUseCase[BookPaginationParams, BookPagination]):
    def __init__(self, *, book_service: BookService) -> None:
        self.book_service = book_service

    async def execute(self, *, input_dto: BookPaginationParams) -> BookPagination:
        return await self.book_service.fetch_book_list(params=input_dto)
