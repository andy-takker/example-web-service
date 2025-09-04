from collections.abc import Sequence
from typing import Final

from library.application.use_case import ICommand
from library.domains.entities.book import CreateBook, UploadBooks
from library.domains.interfaces.clients.open_library import IOpenLibraryClient
from library.domains.services.book import BookService
from library.domains.uow import AbstractUow

BUCKET_SIZE: Final[int] = 100


class UploadBooksCommand(ICommand[UploadBooks, None]):
    def __init__(
        self,
        *,
        uow: AbstractUow,
        book_service: BookService,
        open_library_client: IOpenLibraryClient,
    ) -> None:
        self._uow = uow
        self._book_service = book_service
        self._open_library_client = open_library_client

    async def execute(self, *, input_dto: UploadBooks) -> None:
        books: list[CreateBook] = []
        for query in input_dto.queries:
            books.extend(await self._get_all_books_by_query(query=query))
        book_buckets = [
            books[i : i + BUCKET_SIZE] for i in range(0, len(books), BUCKET_SIZE)
        ]
        async with self._uow:
            for book_bucket in book_buckets:
                await self._book_service.save_bulk_books(books=book_bucket)

    async def _get_all_books_by_query(self, *, query: str) -> Sequence[CreateBook]:
        books: list[CreateBook] = []
        offset = 0
        while True:
            result = await self._open_library_client.search(
                query=query,
                limit=BUCKET_SIZE,
                offset=offset,
            )
            books.extend(
                [
                    CreateBook(
                        title=book.title,
                        year=0,
                        author=",".join(book.authors),
                    )
                    for book in result.books
                ]
            )
            if len(result.books) < BUCKET_SIZE:
                break
            offset += BUCKET_SIZE
        return books
