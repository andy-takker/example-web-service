from library.application.use_case import IQuery
from library.domains.entities.book import BookPagination, BookPaginationParams
from library.domains.services.book import BookService


class FetchBookListQuery(IQuery[BookPaginationParams, BookPagination]):
    __book_service: BookService

    def __init__(self, *, book_service: BookService) -> None:
        self.__book_service = book_service

    async def execute(self, *, input_dto: BookPaginationParams) -> BookPagination:
        return await self.__book_service.fetch_book_list(params=input_dto)
