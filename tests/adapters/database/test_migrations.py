from sqlalchemy.ext.asyncio import AsyncEngine

from library.adapters.database.tables import BaseTable
from tests.utils import get_diff_db_metadata


async def test_migrations_up_to_date(engine: AsyncEngine) -> None:
    async with engine.connect() as connection:
        diff = await connection.run_sync(
            get_diff_db_metadata,
            metadata=(BaseTable.metadata,),
        )
    assert not diff
