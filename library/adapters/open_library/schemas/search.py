from collections.abc import Sequence

from msgspec import Struct


class OpenLibraryDocStruct(Struct):
    title: str
    key: str
    author_name: Sequence[str]


class OpenLibrarySearchStruct(Struct):
    num_found: int
    start: int
    offset: int
    docs: Sequence[OpenLibraryDocStruct]
