from os import environ

import pytest

from library.adapters.nats.config import NatsConfig


@pytest.fixture
def nats_config() -> NatsConfig:
    return NatsConfig(
        host=environ.get("APP_NATS_HOST", "127.0.0.1"),
        port=int(environ.get("APP_NATS_PORT", 4222)),
    )
