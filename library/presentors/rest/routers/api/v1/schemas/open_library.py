from collections.abc import Sequence

from library.presentors.rest.schemas import BaseSchema


class OpenLibraryBookSchema(BaseSchema):
    key: str
    title: str
    authors: Sequence[str]


class OpenLibrarySearchSchema(BaseSchema):
    books: Sequence[OpenLibraryBookSchema]
    total: int
    start: int
    offset: int
