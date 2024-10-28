import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from library.adapters.database.storages.book import BookStorage
from library.domains.interfaces.storages.book import IBookStorage


@pytest.fixture
def book_storage(session: AsyncSession) -> IBookStorage:
    return BookStorage(session=session)
