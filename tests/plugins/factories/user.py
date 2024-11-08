from collections.abc import Callable

import pytest
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from library.adapters.database.tables import UserTable


class UserTableFactory(SQLAlchemyFactory[UserTable]):
    @classmethod
    def deleted_at(cls) -> None:
        return None


@pytest.fixture
def create_user(session: AsyncSession) -> Callable:
    async def _factory(**kwargs) -> UserTable:
        user = UserTableFactory.build(**kwargs)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    return _factory
