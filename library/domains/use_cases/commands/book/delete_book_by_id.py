from dataclasses import dataclass

from library.application.use_case import ICommand
from library.domains.entities.book import BookId
from library.domains.services.book import BookService


@dataclass(frozen=True, kw_only=True, slots=True)
class DeleteBookByIdCommand(ICommand[BookId, None]):
    book_service: BookService

    async def execute(self, *, input_dto: BookId) -> None:
        await self.book_service.delete_book_by_id(book_id=input_dto)
