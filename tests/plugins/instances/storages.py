import pytest

from library.adapters.database.storages.book import BookStorage
from library.adapters.database.storages.user import UserStorage
from library.adapters.database.uow import SqlalchemyUow
from library.domains.interfaces.storages.book import IBookStorage
from library.domains.interfaces.storages.user import IUserStorage


@pytest.fixture
def book_storage(uow: SqlalchemyUow) -> IBookStorage:
    return BookStorage(uow=uow)


@pytest.fixture
def user_storage(uow: SqlalchemyUow) -> IUserStorage:
    return UserStorage(uow=uow)
