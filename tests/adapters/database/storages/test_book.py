from uuid import UUID

from library.domains.entities.book import Book, BookId
from library.domains.interfaces.storages.book import IBookStorage

UUID_1 = UUID(int=1)


async def test_fetch_book_by_id__not_found(book_storage: IBookStorage):
    assert await book_storage.fetch_book_by_id(book_id=BookId(UUID_1)) is None


async def test_fetch_book_by_id__ok(book_storage: IBookStorage, create_book):
    book = await create_book(id=UUID_1)
    storage_book = await book_storage.fetch_book_by_id(book_id=BookId(UUID_1))
    assert storage_book == Book(
        id=book.id,
        title=book.title,
        year=book.year,
        author=book.author,
        created_at=book.created_at,
        updated_at=book.updated_at,
    )
