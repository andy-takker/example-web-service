from dataclasses import dataclass, field
from enum import StrEnum, unique
from os import environ

import sentry_sdk
from sentry_sdk.integrations.asyncio import AsyncioIntegration


@unique
class SentryEnv(StrEnum):
    DEV = "DEV"
    PROD = "PROD"


def setup_sentry(
    dsn: str,
    env: SentryEnv = SentryEnv.DEV,
) -> None:
    if not dsn:
        raise ValueError("APP_SENTRY_DSN is not set")
    sentry_sdk.init(
        dsn=dsn,
        integrations=[AsyncioIntegration()],
        environment=env,
    )


@dataclass(frozen=True, kw_only=True, slots=True)
class SentryConfig:
    dsn: str = field(default_factory=lambda: environ.get("APP_SENTRY_DSN", ""))
    use_sentry: bool = field(
        default_factory=lambda: environ.get("APP_SENTRY_USE", "False").lower() == "true"
    )
    env: SentryEnv = field(
        default_factory=lambda: SentryEnv(
            environ.get("APP_SENTRY_ENV", SentryEnv.DEV).upper()
        )
    )
