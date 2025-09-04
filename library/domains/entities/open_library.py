from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True, slots=True)
class OpenLibrarySearchParams:
    query: str
    limit: int
    offset: int


@dataclass(kw_only=True, frozen=True, slots=True)
class OpenLibraryBook:
    key: str
    title: str
    authors: Sequence[str]


@dataclass(kw_only=True, frozen=True, slots=True)
class OpenLibrarySearchResult:
    books: Sequence[OpenLibraryBook]
    total: int
    start: int
    offset: int
