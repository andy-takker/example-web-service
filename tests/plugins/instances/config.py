import pytest

from library.adapters.database.config import DatabaseConfig
from library.application.config import AppConfig, SecretConfig
from library.presentors.rest.config import RestConfig


@pytest.fixture
def rest_config(db_config: DatabaseConfig) -> RestConfig:
    return RestConfig(
        app=AppConfig(debug=True),
        database=db_config,
        secret=SecretConfig(),
    )
