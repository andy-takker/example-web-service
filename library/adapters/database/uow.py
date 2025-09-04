import asyncio
import logging
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncSessionTransaction,
    async_sessionmaker,
)

from library.domains.uow import AbstractUow

logger = logging.getLogger(__name__)


class SqlalchemyUow(AbstractUow):
    _session: AsyncSession | None
    _transaction: AsyncSessionTransaction | None
    _session_factory: async_sessionmaker[AsyncSession]

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session = None
        self._transaction = None

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise Exception("Session is not created")
        return self._session

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
        self._transaction = None

    async def create_transaction(self) -> None:
        if self._session is not None:
            logger.warning("Attempt to create already existing session")
            if self._transaction is not None:
                raise Exception("Session is already in transaction")
            else:
                self._transaction = await self.session.begin()
        else:
            self._session = self._session_factory()
            self._transaction = await self.session.begin()

    async def close_transaction(self, *exc: Any) -> None:
        task = asyncio.create_task(self.session.close())
        await asyncio.shield(task)
        self._transaction = None
        self._session = None
