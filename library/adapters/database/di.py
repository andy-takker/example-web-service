from collections.abc import AsyncIterator

from dishka import AnyOf, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from library.adapters.database.config import DatabaseConfig
from library.adapters.database.storages.book import BookStorage
from library.adapters.database.storages.user import UserStorage
from library.adapters.database.uow import SqlalchemyUow
from library.adapters.database.utils import create_engine, create_sessionmaker
from library.application.config import AppConfig
from library.domain.interfaces.storages.book import IBookStorage
from library.domain.interfaces.storages.user import IUserStorage
from library.domain.uow import AbstractUow


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def engine(
        self, config: DatabaseConfig, app_config: AppConfig
    ) -> AsyncIterator[AsyncEngine]:
        async with create_engine(
            dsn=config.dsn,
            debug=app_config.debug,
            pool_size=config.pool_size,
            pool_timeout=config.pool_timeout,
            max_overflow=config.max_overflow,
        ) as engine:
            yield engine

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_sessionmaker(engine=engine)

    @provide(scope=Scope.REQUEST)
    def uow(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AnyOf[SqlalchemyUow, AbstractUow]:
        return SqlalchemyUow(session_factory=session_factory)

    @provide(scope=Scope.REQUEST)
    def book_storage(self, uow: SqlalchemyUow) -> IBookStorage:
        return BookStorage(uow=uow)

    @provide(scope=Scope.REQUEST)
    def user_storage(self, uow: SqlalchemyUow) -> IUserStorage:
        return UserStorage(uow=uow)
