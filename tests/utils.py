from collections.abc import Sequence

from alembic.config import Config as AlembicConfig
from alembic.runtime.environment import EnvironmentContext
from alembic.script import ScriptDirectory
from sqlalchemy import Connection, MetaData, pool, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_engine_from_config,
)

TABLES_FOR_TRUNCATE: Sequence[str] = (
    "books",
    # "authors",
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
