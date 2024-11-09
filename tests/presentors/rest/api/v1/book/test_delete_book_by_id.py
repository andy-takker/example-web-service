from http import HTTPStatus
from uuid import UUID

from httpx import AsyncClient
from sqlalchemy import select

from library.adapters.database.tables import BookTable

UUID_1 = UUID(int=1)


def api_url(book_id: UUID) -> str:
    return f"/api/v1/books/{book_id}/"


async def test_delete_book_by_id__ok(create_book, client: AsyncClient):
    await create_book(id=UUID_1)

    response = await client.delete(api_url(book_id=UUID_1))
    assert response.status_code == HTTPStatus.NO_CONTENT


async def test_delete_book_by_id__ok__check_db(
    client: AsyncClient, session, create_book
):
    await create_book(id=UUID_1)
    await client.delete(api_url(book_id=UUID_1))
    stmt = select(BookTable).where(BookTable.id == UUID_1)
    book = (await session.scalars(stmt)).one()
    assert book.deleted_at


async def test_delete_book_by_id__not_found(client: AsyncClient):
    response = await client.delete(api_url(book_id=UUID_1))
    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_delete_book_by_id__double_delete__not_found(
    client: AsyncClient, create_book
):
    await create_book(id=UUID_1)
    await client.delete(api_url(book_id=UUID_1))
    response = await client.delete(api_url(book_id=UUID_1))
    assert response.status_code == HTTPStatus.NOT_FOUND
