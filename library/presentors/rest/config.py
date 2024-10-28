from dataclasses import dataclass, field
from os import environ

from library.adapters.database.config import DatabaseConfig
from library.application.config import AppConfig, LogConfig, SecretConfig


@dataclass
class RestConfig:
    host: str = field(default_factory=lambda: environ.get("APP_REST_HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(environ.get("APP_REST_PORT", 8000)))
    log: LogConfig = field(default_factory=lambda: LogConfig())
    app: AppConfig = field(default_factory=lambda: AppConfig())
    database: DatabaseConfig = field(default_factory=lambda: DatabaseConfig())
    secret: SecretConfig = field(default_factory=lambda: SecretConfig())
