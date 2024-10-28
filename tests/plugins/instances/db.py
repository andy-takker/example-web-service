from collections.abc import AsyncIterator
from os import environ
from types import SimpleNamespace

import pytest
from alembic.config import Config as AlembicConfig
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from library.adapters.database.config import DatabaseConfig
from library.adapters.database.tables import BaseTable
from library.adapters.database.utils import (
    create_engine,
    create_sessionmaker,
    make_alembic_config,
)
from tests.utils import run_async_migrations


@pytest.fixture
def db_config() -> DatabaseConfig:
    return DatabaseConfig(
        dsn=environ.get(
            "APP_DB_DSN",
            "postgresql+asyncpg://library:library@127.0.0.1:5432/library",
        ),
    )


@pytest.fixture
def alembic_config(db_config: DatabaseConfig) -> AlembicConfig:
    cmd_options = SimpleNamespace(
        config="alembic.ini",
        name="alembic",
        raiseerr=False,
        x=None,
    )
    return make_alembic_config(cmd_options, pg_url=db_config.dsn)


@pytest.fixture
async def engine(
    alembic_config: AlembicConfig,
    db_config: DatabaseConfig,
) -> AsyncIterator[AsyncEngine]:
    await run_async_migrations(alembic_config, BaseTable.metadata, "head")
    async with create_engine(dsn=db_config.dsn, debug=False) as engine:
        async with engine.begin() as conn:
            await conn.run_sync(BaseTable.metadata.drop_all)
            await conn.run_sync(BaseTable.metadata.create_all)
        yield engine


@pytest.fixture
def session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return create_sessionmaker(engine=engine)


@pytest.fixture
async def session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session
