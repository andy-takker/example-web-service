import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from library.adapters.database.storages.book import BookStorage
from library.adapters.database.storages.user import UserStorage
from library.domains.interfaces.storages.book import IBookStorage
from library.domains.interfaces.storages.user import IUserStorage


@pytest.fixture
def book_storage(session: AsyncSession) -> IBookStorage:
    return BookStorage(session=session)


@pytest.fixture
def user_storage(session: AsyncSession) -> IUserStorage:
    return UserStorage(session=session)
