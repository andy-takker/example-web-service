from http import HTTPStatus
from uuid import UUID

from dirty_equals import IsDict, IsStr
from httpx import AsyncClient
from sqlalchemy import select

from library.adapters.database.tables import BookTable

UUID_1 = UUID(int=1)


def api_url(book_id: UUID) -> str:
    return f"/api/v1/books/{book_id}/"


async def test_update_book__empty_payload(client: AsyncClient):
    response = await client.patch(api_url(book_id=UUID_1))
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_update_book__not_found(client: AsyncClient):
    response = await client.patch(
        api_url(book_id=UUID_1),
        json={
            "title": "Test book",
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_update_book__ok__status(client: AsyncClient, create_book):
    await create_book(id=UUID_1)
    response = await client.patch(
        api_url(book_id=UUID_1),
        json={
            "title": "Test book",
        },
    )
    assert response.status_code == HTTPStatus.OK


async def test_update_book__ok__format(client: AsyncClient, create_book):
    book = await create_book(id=UUID_1)
    response = await client.patch(
        api_url(book_id=UUID_1),
        json={
            "title": "Test book",
        },
    )
    assert response.json() == IsDict(
        {
            "id": str(book.id),
            "title": "Test book",
            "author": book.author,
            "year": book.year,
            "created_at": IsStr(),
            "updated_at": IsStr(),
        }
    )


async def test_update_book__ok__check_db(client: AsyncClient, session, create_book):
    await create_book(id=UUID_1)
    await client.patch(
        api_url(book_id=UUID_1),
        json={
            "title": "Test book",
        },
    )
    stmt = select(BookTable).where(BookTable.id == UUID_1)
    db_book = (await session.scalars(stmt)).one()
    assert db_book.title == "Test book"


async def test_update_book__conflict(client: AsyncClient, create_book):
    await create_book(author="Already exists author", title="Test title", year=2024)
    await create_book(id=UUID_1, author="Test author", title="Test title", year=2024)

    response = await client.patch(
        api_url(book_id=UUID_1),
        json={
            "author": "Already exists author",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
