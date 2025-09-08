from asyncly.srvmocker import MockService
from faststream.nats import NatsBroker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from library.adapters.database.tables import BookTable
from library.presentors.faststream.handlers.books import upload_open_library_books
from tests.plugins.instances.open_library import OpenLibrarySearchResponse


async def test_upload_books(
    faststream_client: NatsBroker,
    session: AsyncSession,
    open_library_service: MockService,
):
    open_library_service.register(
        "search",
        OpenLibrarySearchResponse(
            books=[
                {
                    "author_name": ["Test author"],
                    "title": "Test title",
                    "key": "test",
                }
            ]
        ),
    )
    await faststream_client.publish(
        message={"queries": ["test"]},
        subject="books.upload_open_library",
        stream="base_stream",
    )
    await upload_open_library_books.wait_call(timeout=3)

    stmt = select(BookTable).where(BookTable.title == "Test title")
    assert (await session.scalars(stmt)).one()
