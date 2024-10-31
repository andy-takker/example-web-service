from http import HTTPStatus
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query

from library.application.exceptions import EmptyPayloadException
from library.domains.entities.book import (
    BookId,
    BookPaginationParams,
    CreateBook,
    UpdateBook,
)
from library.domains.uow import AbstractUow
from library.domains.use_cases.commands.create_book import CreateBookCommand
from library.domains.use_cases.commands.delete_book_by_id import DeleteBookByIdCommand
from library.domains.use_cases.commands.update_book_by_id import UpdateBookByIdCommand
from library.domains.use_cases.queries.fetch_book_by_id import FetchBookByIdQuery
from library.domains.use_cases.queries.fetch_book_list import FetchBookListQuery
from library.presentors.rest.routers.api.v1.schemas.books import (
    BookPaginationParamsSchema,
    BookPaginationSchema,
    BookSchema,
    CreateBookSchema,
    UpdateBookSchema,
)

router = APIRouter(prefix="/books", tags=["Books"], route_class=DishkaRoute)


@router.get(
    "/",
    response_model=BookPaginationSchema,
    status_code=HTTPStatus.OK,
    description="Get books list",
)
async def fetch_books(
    params: BookPaginationParamsSchema = Query(),
    *,
    fetch_book_list: FromDishka[FetchBookListQuery],
    uow: FromDishka[AbstractUow],
) -> BookPaginationSchema:
    async with uow:
        books = await fetch_book_list.execute(
            input_dto=BookPaginationParams(limit=params.limit, offset=params.offset)
        )
    return BookPaginationSchema.model_validate(books)


@router.post(
    "/",
    response_model=BookSchema,
    status_code=HTTPStatus.CREATED,
    description="Create book",
)
async def create_book(
    create_book_data: CreateBookSchema,
    *,
    create_book: FromDishka[CreateBookCommand],
    uow: FromDishka[AbstractUow],
) -> BookSchema:
    async with uow:
        book = await create_book.execute(
            input_dto=CreateBook(
                title=create_book_data.title,
                year=create_book_data.year,
                author=create_book_data.author,
            ),
        )
    return BookSchema.model_validate(book)


@router.get(
    "/{book_id}/",
    response_model=BookSchema,
    status_code=HTTPStatus.OK,
    description="Get book by ID",
)
async def fetch_book(
    book_id: UUID,
    *,
    fetch_book_by_id: FromDishka[FetchBookByIdQuery],
    uow: FromDishka[AbstractUow],
) -> BookSchema:
    async with uow:
        book = await fetch_book_by_id.execute(input_dto=BookId(book_id))
    return BookSchema.model_validate(book)


@router.patch(
    "/{book_id}/",
    response_model=BookSchema,
    status_code=HTTPStatus.OK,
    description="Update book by ID",
)
async def update_book_by_id(
    book_id: UUID,
    update_book_data: UpdateBookSchema,
    *,
    update_book: FromDishka[UpdateBookByIdCommand],
    uow: FromDishka[AbstractUow],
) -> BookSchema:
    values = update_book_data.model_dump(exclude_unset=True)
    if not values:
        raise EmptyPayloadException(message="No values to update")
    async with uow:
        book = await update_book.execute(
            input_dto=UpdateBook(
                book_id=BookId(book_id),
                **values,
            ),
        )
    return BookSchema.model_validate(book)


@router.delete(
    "/{book_id}/",
    status_code=HTTPStatus.NO_CONTENT,
    description="Delete book by ID",
)
async def delete_book_by_id(
    book_id: UUID,
    *,
    delete_book_by_id: FromDishka[DeleteBookByIdCommand],
    uow: FromDishka[AbstractUow],
) -> None:
    async with uow:
        await delete_book_by_id.execute(input_dto=BookId(book_id))
