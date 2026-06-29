from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from dishka.integrations.litestar import FromDishka, inject
from litestar import Controller, delete, get, patch, post
from litestar.params import Parameter

from library.application.exceptions import EmptyPayloadException
from library.domain.entities.book import (
    BookId,
    BookPaginationParams,
    CreateBook,
    UpdateBook,
)
from library.domain.use_cases.commands.book.create_book import CreateBookCommand
from library.domain.use_cases.commands.book.delete_book_by_id import (
    DeleteBookByIdCommand,
)
from library.domain.use_cases.commands.book.update_book_by_id import (
    UpdateBookByIdCommand,
)
from library.domain.use_cases.queries.book.fetch_book_by_id import FetchBookByIdQuery
from library.domain.use_cases.queries.book.fetch_book_list import FetchBookListQuery
from library.presentors.rest.routers.api.v1.schemas.books import (
    BookPaginationSchema,
    BookSchema,
    CreateBookSchema,
    UpdateBookSchema,
)


class BooksController(Controller):
    path = "/books"
    tags = ["Books"]

    @get(
        "/",
        status_code=HTTPStatus.OK,
        description="Get books list",
    )
    @inject
    async def fetch_books(
        self,
        fetch_book_list: FromDishka[FetchBookListQuery],
        limit: Annotated[int, Parameter(ge=1, le=100)] = 10,
        offset: Annotated[int, Parameter(ge=0)] = 0,
    ) -> BookPaginationSchema:
        books = await fetch_book_list.execute(
            input_dto=BookPaginationParams(limit=limit, offset=offset)
        )
        return BookPaginationSchema.model_validate(books)

    @post(
        "/",
        status_code=HTTPStatus.CREATED,
        description="Create book",
    )
    @inject
    async def create_book(
        self,
        data: CreateBookSchema,
        create_book: FromDishka[CreateBookCommand],
    ) -> BookSchema:
        book = await create_book.execute(
            input_dto=CreateBook(
                title=data.title,
                year=data.year,
                author=data.author,
            ),
        )
        return BookSchema.model_validate(book)

    @get(
        "/{book_id:uuid}/",
        status_code=HTTPStatus.OK,
        description="Get book by ID",
    )
    @inject
    async def fetch_book(
        self,
        book_id: UUID,
        fetch_book_by_id: FromDishka[FetchBookByIdQuery],
    ) -> BookSchema:
        book = await fetch_book_by_id.execute(input_dto=BookId(book_id))
        return BookSchema.model_validate(book)

    @patch(
        "/{book_id:uuid}/",
        status_code=HTTPStatus.OK,
        description="Update book by ID",
    )
    @inject
    async def update_book_by_id(
        self,
        update_book: FromDishka[UpdateBookByIdCommand],
        book_id: UUID,
        data: UpdateBookSchema,
    ) -> BookSchema:
        values = data.model_dump(exclude_unset=True)
        if not values:
            raise EmptyPayloadException(message="No values to update")
        book = await update_book.execute(
            input_dto=UpdateBook(
                id=BookId(book_id),
                **values,
            ),
        )
        return BookSchema.model_validate(book)

    @delete(
        "/{book_id:uuid}/",
        status_code=HTTPStatus.NO_CONTENT,
        description="Delete book by ID",
    )
    @inject
    async def delete_book_by_id(
        self,
        book_id: UUID,
        delete_book_by_id: FromDishka[DeleteBookByIdCommand],
    ) -> None:
        await delete_book_by_id.execute(input_dto=BookId(book_id))
