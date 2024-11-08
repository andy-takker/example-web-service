from dataclasses import dataclass, field

from library.adapters.database.config import DatabaseConfig
from library.application.config import AppConfig, SecretConfig


@dataclass
class RestConfig:
    app: AppConfig = field(default_factory=lambda: AppConfig())
    database: DatabaseConfig = field(default_factory=lambda: DatabaseConfig())
    secret: SecretConfig = field(default_factory=lambda: SecretConfig())
