from aiocache import BaseCache
from dishka import BaseScope, Provider, Scope, provide
from dishka.entities.component import Component

from library.adapters.redis.cache import get_redis_cache
from library.adapters.redis.config import RedisConfig


class RedisProvider(Provider):
    def __init__(
        self,
        config: RedisConfig,
        scope: BaseScope | None = None,
        component: Component | None = None,
    ):
        self._config = config
        super().__init__(scope, component)

    @provide(scope=Scope.APP)
    def redis_cache(self) -> BaseCache:
        return get_redis_cache(
            host=self._config.host,
            port=self._config.port,
        )
