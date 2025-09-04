import os
from argparse import Namespace
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from enum import Enum
from pathlib import Path
from typing import Any, Final

import sqlalchemy.dialects.postgresql as pg
from alembic.config import Config
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

PROJECT_PATH: Final = Path(__file__).parent.parent.parent
ALEMBIC_INI_PATH: Final[Path] = PROJECT_PATH / "adapters" / "database" / "alembic.ini"


@asynccontextmanager
async def create_engine(
    dsn: str,
    debug: bool,
    pool_size: int,
    pool_timeout: int,
    max_overflow: int,
) -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(
        url=dsn,
        echo=debug,
        pool_size=pool_size,
        pool_timeout=pool_timeout,
        max_overflow=max_overflow,
        pool_pre_ping=True,
    )
    yield engine
    await engine.dispose()


def create_sessionmaker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


def make_alembic_config(cmd_opts: Namespace, pg_url: str) -> Config:
    config = Config(
        file_=ALEMBIC_INI_PATH,
        ini_section=cmd_opts.name,
        cmd_opts=cmd_opts,
    )

    alembic_location = config.get_main_option("script_location")
    if not alembic_location:
        raise ValueError

    if not os.path.isabs(alembic_location):
        config.set_main_option("script_location", str(PROJECT_PATH / alembic_location))

    config.set_main_option("sqlalchemy.url", pg_url)

    config.attributes["configure_logger"] = False

    return config


def make_pg_enum(enum_cls: type[Enum], **kwargs: Any) -> pg.ENUM:
    return pg.ENUM(
        enum_cls,
        values_callable=_choices,
        **kwargs,
    )


def _choices(enum_cls: type[Enum]) -> tuple[str, ...]:
    return tuple(map(str, enum_cls))
