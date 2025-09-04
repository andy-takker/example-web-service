from dataclasses import dataclass, field

from library.adapters.database.config import DatabaseConfig
from library.adapters.nats.config import NatsConfig
from library.adapters.open_library.config import OpenLibraryConfig
from library.adapters.redis.config import RedisConfig
from library.application.config import AppConfig, SecretConfig
from library.application.logging import LoggingConfig


@dataclass(frozen=True, kw_only=True, slots=True)
class Config:
    app: AppConfig = field(default_factory=lambda: AppConfig())
    database: DatabaseConfig = field(default_factory=lambda: DatabaseConfig())
    log: LoggingConfig = field(default_factory=lambda: LoggingConfig())
    nats: NatsConfig = field(default_factory=lambda: NatsConfig())
    open_library: OpenLibraryConfig = field(default_factory=lambda: OpenLibraryConfig())
    redis: RedisConfig = field(default_factory=lambda: RedisConfig())
    secret: SecretConfig = field(default_factory=lambda: SecretConfig())
