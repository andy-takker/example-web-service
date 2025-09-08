from collections.abc import Sequence
from datetime import UTC, datetime
from typing import NoReturn

from sqlalchemy import exists, func, insert, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import DBAPIError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from library.adapters.database.tables import BookTable
from library.adapters.database.uow import SqlalchemyUow
from library.application.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
    LibraryException,
)
from library.domains.entities.book import (
    Book,
    BookId,
    BookPaginationParams,
    CreateBook,
    UpdateBook,
)


class BookStorage:
    def __init__(self, *, uow: SqlalchemyUow) -> None:
        self._uow = uow

    @property
    def _session(self) -> AsyncSession:
        return self._uow.session

    async def fetch_book_by_id(self, *, book_id: BookId) -> Book | None:
        query = select(BookTable).where(
            BookTable.id == book_id,
            BookTable.deleted_at.is_(None),
        )
        book = (await self._session.scalars(query)).first()

        if book is None:
            return None
        return Book(
            id=BookId(book.id),
            title=book.title,
            year=book.year,
            author=book.author,
            created_at=book.created_at,
            updated_at=book.updated_at,
        )

    async def exists_book_by_id(self, *, book_id: BookId) -> bool:
        stmt = select(
            exists().where(BookTable.id == book_id, BookTable.deleted_at.is_(None))
        )
        return bool((await self._session.execute(stmt)).scalar())

    async def count_books(self, *, params: BookPaginationParams) -> int:
        query = (
            select(func.count())
            .select_from(BookTable)
            .where(BookTable.deleted_at.is_(None))
        )
        result = (await self._session.execute(query)).scalar()
        return result or 0

    async def fetch_book_list(self, *, params: BookPaginationParams) -> Sequence[Book]:
        query = (
            select(
                BookTable.id,
                BookTable.title,
                BookTable.year,
                BookTable.author,
                BookTable.created_at,
                BookTable.updated_at,
            )
            .where(BookTable.deleted_at.is_(None))
            .limit(params.limit)
            .offset(params.offset)
            .order_by(BookTable.id)
        )
        result = (await self._session.execute(query)).mappings().all()
        return [
            Book(
                id=book["id"],
                title=book["title"],
                year=book["year"],
                author=book["author"],
                created_at=book["created_at"],
                updated_at=book["updated_at"],
            )
            for book in result
        ]

    async def create_book(self, *, book: CreateBook) -> Book:
        stmt = (
            insert(BookTable)
            .values(
                title=book.title,
                year=book.year,
                author=book.author,
            )
            .returning(
                BookTable.id,
                BookTable.title,
                BookTable.year,
                BookTable.author,
                BookTable.created_at,
                BookTable.updated_at,
            )
        )
        try:
            result = (await self._session.execute(stmt)).mappings().one()
        except IntegrityError as e:
            self._raise_error(e)
        return Book(
            id=BookId(result["id"]),
            title=result["title"],
            year=result["year"],
            author=result["author"],
            created_at=result["created_at"],
            updated_at=result["updated_at"],
        )

    async def delete_book_by_id(self, *, book_id: BookId) -> None:
        stmt = (
            update(BookTable)
            .where(BookTable.id == book_id)
            .values(deleted_at=datetime.now(tz=UTC))
        )
        await self._session.execute(stmt)

    async def update_book_by_id(self, *, update_book: UpdateBook) -> Book:
        stmt = (
            update(BookTable)
            .where(BookTable.id == update_book.id)
            .values(**update_book.to_dict())
            .returning(
                BookTable.id,
                BookTable.title,
                BookTable.year,
                BookTable.author,
                BookTable.created_at,
                BookTable.updated_at,
            )
        )
        try:
            result = (await self._session.execute(stmt)).mappings().one()
        except NoResultFound as e:
            raise EntityNotFoundException(entity=Book, entity_id=update_book.id) from e
        except IntegrityError as e:
            self._raise_error(e)
        return Book(
            id=BookId(result["id"]),
            title=result["title"],
            year=result["year"],
            author=result["author"],
            created_at=result["created_at"],
            updated_at=result["updated_at"],
        )

    async def save_bulk_books(self, *, books: Sequence[CreateBook]) -> None:
        stmt = pg_insert(BookTable).values(
            [
                {
                    "title": book.title,
                    "year": book.year,
                    "author": book.author,
                }
                for book in books
            ]
        )
        stmt = stmt.on_conflict_do_nothing(
            index_elements=[
                BookTable.title,
                BookTable.year,
                BookTable.author,
            ],
            index_where=BookTable.deleted_at.is_(None),
        )
        await self._session.execute(stmt)

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        if constraint == "ix__books__title_year_author":
            raise EntityAlreadyExistsException("Book already exists") from e
        raise LibraryException(message="Unknown error") from e
