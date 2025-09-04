from dataclasses import dataclass, field
from os import environ


@dataclass(frozen=True, kw_only=True, slots=True)
class NatsConfig:
    host: str = field(default_factory=lambda: environ["APP_NATS_HOST"])
    port: int = field(default_factory=lambda: int(environ["APP_NATS_PORT"]))
    name: str = field(
        default_factory=lambda: environ.get("APP_NATS_NAME", "exchange_service")
    )
    connect_timeout: int = field(
        default_factory=lambda: int(environ.get("APP_NATS_CONNECT_TIMEOUT", 5))
    )
    reconnect_time_wait: int = field(
        default_factory=lambda: int(environ.get("APP_NATS_RECONNECT_TIME_WAIT", 5))
    )
    max_reconnect_attempts: int = field(
        default_factory=lambda: int(environ.get("APP_NATS_MAX_RECONNECT_ATTEMPTS", 5))
    )
    allow_reconnect: bool = field(
        default_factory=lambda: environ.get("APP_NATS_ALLOW_RECONNECT", "true").lower()
        == "true"
    )

    @property
    def dsn(self) -> str:
        return f"nats://{self.host}:{self.port}"
