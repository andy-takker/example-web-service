from dataclasses import dataclass, field

from library.adapters.database.config import DatabaseConfig
from library.application.config import AppConfig, SecretConfig
from library.application.logging import LoggingConfig


@dataclass(frozen=True, kw_only=True, slots=True)
class RestConfig:
    log: LoggingConfig = field(default_factory=lambda: LoggingConfig())
    app: AppConfig = field(default_factory=lambda: AppConfig())
    database: DatabaseConfig = field(default_factory=lambda: DatabaseConfig())
    secret: SecretConfig = field(default_factory=lambda: SecretConfig())
