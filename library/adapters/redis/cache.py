from aiocache import RedisCache
from aiocache.serializers import PickleSerializer


def get_redis_cache(
    host: str,
    port: int,
) -> RedisCache:
    return RedisCache(
        endpoint=host,
        port=port,
        serializer=PickleSerializer(),
    )
