import abc
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Concatenate, ParamSpec, TypeVar

from aiocache import BaseCache

P = ParamSpec("P")
RT = TypeVar("RT")


class ICached(abc.ABC):
    _cache: BaseCache


def cached(key_func: Callable[..., str] | None = None, ttl: int = 60 * 60) -> Callable:
    def decorator(
        func: Callable[Concatenate[ICached, P], Awaitable[RT]],
    ) -> Callable[Concatenate[ICached, P], Awaitable[RT]]:
        @wraps(func)
        async def wrapped(self: ICached, *args: P.args, **kwargs: P.kwargs) -> RT:
            key = (
                key_func(*args, **kwargs)
                if key_func
                else f"{self.__class__.__name__}:{func.__name__}:{args}:{kwargs}"
            )

            cached_result = await self._cache.get(key)
            if cached_result is not None:
                return cached_result
            result = await func(self, *args, **kwargs)
            await self._cache.set(key, result, ttl=ttl)
            return result

        return wrapped

    return decorator
