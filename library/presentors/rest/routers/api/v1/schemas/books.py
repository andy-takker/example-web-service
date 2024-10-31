from collections.abc import Sequence
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from library.domains.entities.book import BookId


class BookSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: BookId
    title: str
    year: int
    author: str
    created_at: datetime
    updated_at: datetime


class BookPaginationParamsSchema(BaseModel):
    limit: PositiveInt = Field(le=100, default=10)
    offset: int = Field(ge=0, default=0)


class BookPaginationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total: int
    items: Sequence[BookSchema]


class CreateBookSchema(BaseModel):
    title: str
    year: PositiveInt
    author: str


class UpdateBookSchema(BaseModel):
    title: str | None = None
    year: int | None = None
    author: str | None = None
