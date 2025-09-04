from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from uuid import UUID

from library.application.entities import UNSET

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
    id: BookId
    title: str = UNSET
    year: int = UNSET
    author: str = UNSET

    def to_dict(self) -> Mapping[str, int | str]:
        values: dict[str, int | str] = {}
        if self.title is not UNSET:
            values["title"] = self.title
        if self.year is not UNSET:
            values["year"] = self.year
        if self.author is not UNSET:
            values["author"] = self.author
        return values
