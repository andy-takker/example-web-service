from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from uuid import UUID

BookId = NewType("BookId", UUID)


@dataclass(frozen=True, kw_only=True, slots=True)
class Book:
    id: BookId
    title: str
    year: int
    author: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class BookPaginationParams:
    limit: int
    offset: int


@dataclass(frozen=True, kw_only=True, slots=True)
class BookPagination:
    total: int
    items: Sequence[Book]
