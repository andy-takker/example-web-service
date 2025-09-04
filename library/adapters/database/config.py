from dataclasses import dataclass, field
from os import environ


@dataclass(frozen=True, kw_only=True, slots=True)
class DatabaseConfig:
    host: str = field(default_factory=lambda: environ["APP_DATABASE_HOST"])
    port: int = field(default_factory=lambda: int(environ["APP_DATABASE_PORT"]))
    user: str = field(default_factory=lambda: environ["APP_DATABASE_USER"])
    password: str = field(default_factory=lambda: environ["APP_DATABASE_PASSWORD"])
    name: str = field(default_factory=lambda: environ["APP_DATABASE_NAME"])
    pool_size: int = field(
        default_factory=lambda: int(environ.get("APP_DATABASE_POOL_SIZE", 10))
    )
    pool_timeout: int = field(
        default_factory=lambda: int(environ.get("APP_DATABASE_POOL_TIMEOUT", 10))
    )
    max_overflow: int = field(
        default_factory=lambda: int(environ.get("APP_DATABASE_MAX_OVERFLOW", 10))
    )

    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
