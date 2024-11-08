import logging
from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any, Self

log = logging.getLogger(__name__)


class AbstractUow(ABC):
    async def __aenter__(self) -> Self:
        await self.create_transaction()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_val:
            log.info("Rolling back transaction due to exception")
            await self.rollback()
        else:
            await self.commit()
        await self.close_transaction(exc_type, exc_val, exc_tb)

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def create_transaction(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close_transaction(self, *exc: Any) -> None:
        raise NotImplementedError
