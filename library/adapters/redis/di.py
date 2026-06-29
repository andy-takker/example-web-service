from collections.abc import AsyncIterator

from aiocache import BaseCache
from dishka import Provider, Scope, provide

from library.adapters.redis.cache import get_redis_cache
from library.adapters.redis.config import RedisConfig


class RedisProvider(Provider):
    scope = Scope.APP

    @provide()
    async def redis_cache(self, config: RedisConfig) -> AsyncIterator[BaseCache]:
        redis_cache = get_redis_cache(
            host=config.host,
            port=config.port,
        )
        yield redis_cache
        await redis_cache.close()
