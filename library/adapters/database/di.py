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
        scope: BaseScope | None = None,
        component: Component | None = None,
    ) -> None:
        self.dsn = dsn
        self.debug = debug
        super().__init__(scope=scope, component=component)

    @provide(scope=Scope.APP)
    async def engine(self) -> AsyncIterator[AsyncEngine]:
        async with create_engine(dsn=self.dsn, debug=self.debug) as engine:
            yield engine

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_sessionmaker(engine=engine)

    @provide(scope=Scope.REQUEST)
    def uow(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AnyOf[SqlalchemyUow, AbstractUow]:
        return SqlalchemyUow(session=session_factory())

    @provide(scope=Scope.REQUEST)
    def book_storage(self, uow: SqlalchemyUow) -> IBookStorage:
        return BookStorage(session=uow.session)

    @provide(scope=Scope.REQUEST)
    def user_storage(self, uow: SqlalchemyUow) -> IUserStorage:
        return UserStorage(session=uow.session)
