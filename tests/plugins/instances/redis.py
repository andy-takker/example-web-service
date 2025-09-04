from collections.abc import AsyncIterator
from os import environ

import pytest
from aiocache import BaseCache
from redis.asyncio import Redis

from library.adapters.redis.cache import get_redis_cache
from library.adapters.redis.config import RedisConfig


@pytest.fixture
def redis_config() -> RedisConfig:
    return RedisConfig(
        host=environ.get("APP_REDIS_HOST", "127.0.0.1"),
        port=int(environ.get("APP_REDIS_PORT", 6379)),
    )


@pytest.fixture
async def clear_redis_cache(redis_config: RedisConfig) -> AsyncIterator[None]:
    redis = Redis.from_url(redis_config.dsn)
    await redis.flushall()
    yield
    await redis.aclose()


@pytest.fixture
def redis_cache(redis_config: RedisConfig, clear_redis_cache) -> BaseCache:
    return get_redis_cache(
        host=redis_config.host,
        port=redis_config.port,
    )
