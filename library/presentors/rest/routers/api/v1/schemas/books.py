from collections.abc import Sequence
from datetime import datetime

from pydantic import PositiveInt

from library.domain.entities.book import BookId
from library.presentors.rest.schemas import BaseSchema


class BookSchema(BaseSchema):
    id: BookId
    title: str
    year: int
    author: str
    created_at: datetime
    updated_at: datetime


class BookPaginationSchema(BaseSchema):
    total: int
    items: Sequence[BookSchema]


class CreateBookSchema(BaseSchema):
    title: str
    year: PositiveInt
    author: str


class UpdateBookSchema(BaseSchema):
    title: str | None = None
    year: int | None = None
    author: str | None = None
