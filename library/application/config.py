from dataclasses import dataclass, field
from os import environ


@dataclass(frozen=True, kw_only=True, slots=True)
class AppConfig:
    title: str = field(default_factory=lambda: environ.get("APP_TITLE", "Library"))
    description: str = field(
        default_factory=lambda: environ.get(
            "APP_DESCRIPTION", "Web application for library"
        )
    )
    version: str = field(default_factory=lambda: environ.get("APP_VERSION", "1.0.0"))
    debug: bool = field(
        default_factory=lambda: environ.get("APP_DEBUG", "False").lower() == "true"
    )


@dataclass(frozen=True, kw_only=True, slots=True)
class SecretConfig:
    secret: str = field(default_factory=lambda: environ.get("APP_SECRET", "secret"))
