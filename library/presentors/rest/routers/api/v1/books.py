from http import HTTPStatus
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query

from library.domains.entities.book import BookId, BookPaginationParams
from library.domains.uow import AbstractUow
from library.domains.use_cases.queries.fetch_book_by_id import FetchBookById
from library.domains.use_cases.queries.fetch_book_list import FetchBookList
from library.presentors.rest.routers.api.v1.schemas.books import (
    BookPaginationParamsSchema,
    BookPaginationSchema,
    BookSchema,
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
    fetch_book_list: FromDishka[FetchBookList],
    uow: FromDishka[AbstractUow],
) -> BookPaginationSchema:
    async with uow:
        books = await fetch_book_list.execute(
            input_dto=BookPaginationParams(limit=params.limit, offset=params.offset)
        )
    return BookPaginationSchema.model_validate(books)


@router.get(
    "/{book_id}",
    response_model=BookSchema,
    status_code=HTTPStatus.OK,
    description="Get book by ID",
)
async def fetch_book(
    book_id: UUID,
    *,
    fetch_book_by_id: FromDishka[FetchBookById],
    uow: FromDishka[AbstractUow],
) -> BookSchema:
    async with uow:
        book = await fetch_book_by_id.execute(input_dto=BookId(book_id))
    return BookSchema.model_validate(book)
