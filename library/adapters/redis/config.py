import os
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True, kw_only=True)
class RedisConfig:
    host: str = field(default_factory=lambda: os.environ["APP_REDIS_HOST"])
    port: int = field(default_factory=lambda: int(os.environ["APP_REDIS_PORT"]))

    @property
    def dsn(self) -> str:
        return f"redis://{self.host}:{self.port}"
