from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from library.adapters.database.tables import BookTable
from library.domains.entities.book import Book, BookId, BookPaginationParams
from library.domains.interfaces.storages.book import IBookStorage


class BookStorage(IBookStorage):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def fetch_book_by_id(self, *, book_id: BookId) -> Book | None:
        query = select(BookTable).where(
            BookTable.id == book_id,
            BookTable.deleted_at.is_(None),
        )
        book = (await self.session.scalars(query)).first()

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

    async def count_books(self, *, params: BookPaginationParams) -> int:
        query = (
            select(func.count())
            .select_from(BookTable)
            .where(BookTable.deleted_at.is_(None))
        )
        result = (await self.session.execute(query)).scalar()
        return result or 0

    async def fetch_book_list(self, *, params: BookPaginationParams) -> Sequence[Book]:
        query = (
            select(BookTable)
            .where(BookTable.deleted_at.is_(None))
            .limit(params.limit)
            .offset(params.offset)
        )
        result = (await self.session.execute(query)).mappings().all()
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
