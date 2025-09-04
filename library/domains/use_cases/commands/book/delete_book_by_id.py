from library.application.use_case import ICommand
from library.domains.entities.book import BookId
from library.domains.services.book import BookService
from library.domains.uow import AbstractUow


class DeleteBookByIdCommand(ICommand[BookId, None]):
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

    async def execute(self, *, input_dto: BookId) -> None:
        async with self._uow:
            await self._book_service.delete_book_by_id(book_id=input_dto)
