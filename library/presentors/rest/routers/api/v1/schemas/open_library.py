from collections.abc import Sequence

from pydantic import BaseModel, ConfigDict


class OpenLibraryBookSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key: str
    title: str
    authors: Sequence[str]


class OpenLibrarySearchSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    books: Sequence[OpenLibraryBookSchema]
    total: int
    start: int
    offset: int
