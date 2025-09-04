from collections.abc import AsyncIterator

from dishka import AnyOf, BaseScope, Component, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from library.adapters.database.storages.book import BookStorage
from library.adapters.database.storages.user import UserStorage
from library.adapters.database.uow import SqlalchemyUow
from library.adapters.database.utils import create_engine, create_sessionmaker
from library.domains.interfaces.storages.book import IBookStorage
from library.domains.interfaces.storages.user import IUserStorage
from library.domains.uow import AbstractUow


class DatabaseProvider(Provider):
    def __init__(
        self,
        dsn: str,
        debug: bool,
        pool_size: int,
        pool_timeout: int,
        max_overflow: int,
        scope: BaseScope | None = None,
        component: Component | None = None,
    ) -> None:
        self._dsn = dsn
        self._debug = debug
        self._pool_size = pool_size
        self._pool_timeout = pool_timeout
        self._max_overflow = max_overflow
        super().__init__(scope=scope, component=component)

    @provide(scope=Scope.APP)
    async def engine(self) -> AsyncIterator[AsyncEngine]:
        async with create_engine(
            dsn=self._dsn,
            debug=self._debug,
            pool_size=self._pool_size,
            pool_timeout=self._pool_timeout,
            max_overflow=self._max_overflow,
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
