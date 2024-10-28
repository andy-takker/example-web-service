from collections.abc import Callable

import pytest
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from library.adapters.database.tables import BookTable


class BookTableFactory(SQLAlchemyFactory[BookTable]): ...


@pytest.fixture
def create_book(session: AsyncSession) -> Callable:
    async def _factory(**kwargs) -> BookTable:
        book = BookTableFactory.build(**kwargs)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    return _factory
