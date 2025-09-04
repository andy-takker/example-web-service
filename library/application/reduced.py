import abc
import asyncio
from collections.abc import Awaitable, Callable, Coroutine
from functools import partial, wraps
from typing import Any, Concatenate, ParamSpec, TypeVar

RT = TypeVar("RT")


class AsyncReducer:
    def __init__(self) -> None:
        self._running: dict[str, asyncio.Future] = {}
        self._tasks: set[asyncio.Task] = set()

    def __call__(self, coro: Coroutine[Any, Any, RT], *, ident: str) -> Awaitable[RT]:
        future, created = self._get_or_create_future(ident)

        if created:
            self._running[ident] = future
            coro_runner = self._runner(ident, coro, future)

            task = asyncio.create_task(coro_runner)
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)
        else:
            coro.close()
            del coro

        return self._waiter(future)

    def _get_or_create_future(self, ident: str) -> tuple[asyncio.Future, bool]:
        f = self._running.get(ident, None)
        if f is not None:
            return f, False
        else:
            f = asyncio.Future()
            self._running[ident] = f
            return f, True

    async def _runner(
        self,
        ident: str,
        coro: Coroutine[Any, Any, RT],
        future: asyncio.Future,
    ) -> None:
        try:
            result = await coro
        except (Exception, asyncio.CancelledError) as e:
            future.set_exception(e)
        else:
            future.set_result(result)
        finally:
            del self._running[ident]

    @classmethod
    async def _waiter(cls, future: asyncio.Future) -> RT:
        wait_future: asyncio.Future = asyncio.Future()

        future.add_done_callback(
            partial(cls._set_wait_future_result, wait_future=wait_future)
        )

        return await wait_future

    @staticmethod
    def _set_wait_future_result(
        result_future: asyncio.Future, wait_future: asyncio.Future
    ) -> None:
        if wait_future.cancelled():
            return

        try:
            result = result_future.result()
            set_func = wait_future.set_result
        except (Exception, asyncio.CancelledError) as e:
            result = e
            set_func = wait_future.set_exception

        set_func(result)


class IReduced(abc.ABC):
    _reducer: AsyncReducer


P = ParamSpec("P")


def reduced(
    key_func: Callable[..., str] | None = None,
) -> Callable:
    def decorator(
        func: Callable[Concatenate[IReduced, P], Coroutine[Any, Any, RT]],
    ) -> Callable[Concatenate[IReduced, P], Coroutine[Any, Any, RT]]:
        @wraps(func)
        async def wrapped(self: IReduced, *args: P.args, **kwargs: P.kwargs) -> RT:
            key = (
                key_func(*args, **kwargs)
                if key_func
                else f"{self.__class__.__name__}:{func.__name__}:{args}:{kwargs}"
            )
            return await self._reducer(func(self, *args, **kwargs), ident=key)

        return wrapped

    return decorator
