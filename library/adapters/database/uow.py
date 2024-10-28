import asyncio
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from library.domains.uow import AbstractUow


class SqlalchemyUow(AbstractUow):
    transaction: AsyncSessionTransaction | None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.transaction = None

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
        self.transaction = None

    async def create_transaction(self) -> None:
        self.transaction = await self.session.begin()

    async def close_transaction(self, *exc: Any) -> None:
        task = asyncio.create_task(self.session.close())
        await asyncio.shield(task)
