from datetime import UTC, datetime
from uuid import UUID

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from library.adapters.database.tables import BookTable
from library.adapters.database.uow import SqlalchemyUow
from library.application.exceptions import EntityNotFoundException
from library.domains.entities.book import (
    Book,
    BookId,
    BookPaginationParams,
    CreateBook,
    UpdateBook,
)
from library.domains.interfaces.storages.book import IBookStorage

UUID_1 = UUID(int=1)
UUID_2 = UUID(int=2)


async def test_fetch_book_by_id__not_found(
    uow: SqlalchemyUow, book_storage: IBookStorage
):
    async with uow:
        assert await book_storage.fetch_book_by_id(book_id=BookId(UUID_1)) is None


async def test_fetch_book_by_id__was_deleted(
    uow: SqlalchemyUow, book_storage: IBookStorage, create_book
):
    await create_book(id=UUID_1, deleted_at=datetime.now(tz=UTC))
    async with uow:
        assert await book_storage.fetch_book_by_id(book_id=BookId(UUID_1)) is None


async def test_fetch_book_by_id__ok(
    uow: SqlalchemyUow, book_storage: IBookStorage, create_book
):
    book = await create_book(id=UUID_1)
    async with uow:
        storage_book = await book_storage.fetch_book_by_id(book_id=BookId(UUID_1))
    assert storage_book == Book(
        id=book.id,
        title=book.title,
        year=book.year,
        author=book.author,
        created_at=book.created_at,
        updated_at=book.updated_at,
    )


async def test_exists_book_by_id__not_found(
    uow: SqlalchemyUow, book_storage: IBookStorage
):
    async with uow:
        assert await book_storage.exists_book_by_id(book_id=BookId(UUID_1)) is False


async def test_exists_book_by_id__was_deleted(
    uow: SqlalchemyUow, book_storage: IBookStorage, create_book
):
    await create_book(id=UUID_1, deleted_at=datetime.now(tz=UTC))
    async with uow:
        assert await book_storage.exists_book_by_id(book_id=BookId(UUID_1)) is False


async def test_exists_book_by_id__ok(
    uow: SqlalchemyUow, book_storage: IBookStorage, create_book
):
    await create_book(id=UUID_1)
    async with uow:
        assert await book_storage.exists_book_by_id(book_id=BookId(UUID_1))


async def test_fetch_book_list__ok(
    uow: SqlalchemyUow, book_storage: IBookStorage, create_book
):
    books = [
        await create_book(id=UUID_1),
        await create_book(id=UUID_2),
    ]
    async with uow:
        db_books = await book_storage.fetch_book_list(
            params=BookPaginationParams(limit=10, offset=0)
        )
    assert db_books == [
        Book(
            id=book.id,
            title=book.title,
            year=book.year,
            author=book.author,
            created_at=book.created_at,
            updated_at=book.updated_at,
        )
        for book in books
    ]


async def test_book_list__with_offset(
    uow: SqlalchemyUow, book_storage: IBookStorage, create_book
):
    await create_book(id=UUID_1)
    book = await create_book(id=UUID_2)
    async with uow:
        assert await book_storage.fetch_book_list(
            params=BookPaginationParams(limit=10, offset=1)
        ) == [
            Book(
                id=book.id,
                title=book.title,
                year=book.year,
                author=book.author,
                created_at=book.created_at,
                updated_at=book.updated_at,
            )
        ]


async def test_book_list__with_limit(
    uow: SqlalchemyUow, book_storage: IBookStorage, create_book
):
    book = await create_book(id=UUID_1)
    await create_book(id=UUID_2)
    async with uow:
        assert await book_storage.fetch_book_list(
            params=BookPaginationParams(limit=1, offset=0)
        ) == [
            Book(
                id=book.id,
                title=book.title,
                year=book.year,
                author=book.author,
                created_at=book.created_at,
                updated_at=book.updated_at,
            )
        ]


async def test_count_books__ok(
    uow: SqlalchemyUow, book_storage: IBookStorage, create_book
):
    await create_book(id=UUID_1)
    await create_book(id=UUID_2)
    async with uow:
        assert (
            await book_storage.count_books(
                params=BookPaginationParams(limit=10, offset=0)
            )
            == 2
        )


async def test_create_book__ok(uow: SqlalchemyUow, book_storage: IBookStorage, session):
    async with uow:
        book = await book_storage.create_book(
            book=CreateBook(
                title="title",
                year=2020,
                author="author",
            )
        )

    stmt = select(BookTable).where(BookTable.id == book.id)
    db_book = (await session.scalars(stmt)).first()
    assert book == Book(
        id=BookId(db_book.id),
        title=db_book.title,
        year=db_book.year,
        author=db_book.author,
        created_at=db_book.created_at,
        updated_at=db_book.updated_at,
    )


async def test_delete_book_by_id__ok(
    uow: SqlalchemyUow, book_storage: IBookStorage, create_book, session: AsyncSession
):
    book = await create_book(id=UUID_1)

    async with uow:
        await book_storage.delete_book_by_id(book_id=book.id)

    stmt = select(BookTable.deleted_at).where(BookTable.id == book.id)
    book_deleted_at = await session.scalar(stmt)

    assert book_deleted_at is not None


async def test_delete_book_by_id__not_found(
    uow: SqlalchemyUow, book_storage: IBookStorage
):
    async with uow:
        assert await book_storage.delete_book_by_id(book_id=BookId(UUID_1)) is None


async def test_update_book_by_id__ok(
    uow: SqlalchemyUow, book_storage: IBookStorage, create_book, session: AsyncSession
):
    book = await create_book(id=UUID_1, title="Old title")

    async with uow:
        await book_storage.update_book_by_id(
            update_book=UpdateBook(
                id=book.id,
                title="New title",
            )
        )

    stmt = select(BookTable.title).where(BookTable.id == book.id)
    book_title = await session.scalar(stmt)
    assert book_title == "New title"


async def test_update_book_by_id__not_found(
    uow: SqlalchemyUow, book_storage: IBookStorage
):
    async with uow:
        with pytest.raises(EntityNotFoundException):
            await book_storage.update_book_by_id(
                update_book=UpdateBook(id=BookId(UUID_1), title="New title")
            ) is None
