from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from uuid import UUID

from library.application.entities import UNSET, Unset

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


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateBook:
    title: str
    year: int
    author: str


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateBook:
    book_id: BookId
    title: str | Unset = UNSET
    year: int | Unset = UNSET
    author: str | Unset = UNSET

    def to_dict(self) -> Mapping[str, int | str]:
        values: dict[str, int | str] = {}
        if not isinstance(self.title, Unset):
            values["title"] = self.title
        if not isinstance(self.year, Unset):
            values["year"] = self.year
        if not isinstance(self.author, Unset):
            values["author"] = self.author
        return values
