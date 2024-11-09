from collections.abc import Callable, Sequence

from alembic.autogenerate import compare_metadata
from alembic.config import Config as AlembicConfig
from alembic.runtime.environment import EnvironmentContext
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from polyfactory import Use
from sqlalchemy import Connection, MetaData, pool, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_engine_from_config,
)

TABLES_FOR_TRUNCATE: Sequence[str] = (
    "books",
    "users",
)


async def truncate_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        for table in TABLES_FOR_TRUNCATE:
            await conn.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))

        await conn.commit()


async def run_async_migrations(
    config: AlembicConfig,
    target_metadata: MetaData,
    revision: str,
) -> None:
    script = ScriptDirectory.from_config(config)

    def upgrade(rev, context):
        return script._upgrade_revs(revision, rev)

    with EnvironmentContext(
        config,
        script=script,
        fn=upgrade,
        as_sql=False,
        starting_rev=None,
        destination_rev=revision,
    ) as context:
        engine = async_engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
        async with engine.connect() as connection:
            await connection.run_sync(
                _do_run_migrations,
                target_metadata=target_metadata,
                context=context,
            )


def _do_run_migrations(
    connection: Connection,
    target_metadata: MetaData,
    context: EnvironmentContext,
) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def get_diff_db_metadata(connection: Connection, metadata: MetaData):
    migration_ctx = MigrationContext.configure(connection)
    return compare_metadata(context=migration_ctx, metadata=metadata)


class IterUse[T](Use):
    def __init__(self, func: Callable[[int], T]) -> None:
        super().__init__(self.next)
        self.count = 0
        self.func = func

    def next(self) -> T:
        self.count += 1
        return self.func(self.count)
