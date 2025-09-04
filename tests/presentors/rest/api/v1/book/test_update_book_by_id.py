from http import HTTPStatus
from uuid import UUID, uuid4

from dirty_equals import IsDatetime, IsDict
from httpx import AsyncClient
from sqlalchemy import select

from library.adapters.database.tables import BookTable


def api_url(book_id: UUID | None = None) -> str:
    if book_id is None:
        book_id = uuid4()
    return f"/api/v1/books/{book_id}/"


async def test_update_book__empty_payload(client: AsyncClient):
    response = await client.patch(api_url())
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_update_book__nothing_to_update(client: AsyncClient):
    response = await client.patch(api_url(), json={})
    assert response.status_code == HTTPStatus.BAD_REQUEST


async def test_update_book__not_found(client: AsyncClient):
    response = await client.patch(
        api_url(),
        json={
            "title": "Test book",
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_update_book__ok__status(client: AsyncClient, create_book):
    book = await create_book()
    response = await client.patch(
        api_url(book.id),
        json={
            "title": "Test book",
        },
    )
    assert response.status_code == HTTPStatus.OK


async def test_update_book__ok__format(client: AsyncClient, create_book):
    book = await create_book()
    response = await client.patch(
        api_url(book.id),
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
            "created_at": IsDatetime(iso_string=True),
            "updated_at": IsDatetime(iso_string=True),
        }
    )


async def test_update_book__ok__check_db(client: AsyncClient, session, create_book):
    book = await create_book()
    await client.patch(
        api_url(book.id),
        json={
            "title": "Test book",
        },
    )
    stmt = select(BookTable.title).where(BookTable.id == book.id)
    title = (await session.scalars(stmt)).one()
    assert title == "Test book"


async def test_update_book__conflict(client: AsyncClient, create_book):
    await create_book(author="Already exists author", title="Test title", year=2024)
    book = await create_book(author="Test author", title="Test title", year=2024)

    response = await client.patch(
        api_url(book_id=book.id),
        json={
            "author": "Already exists author",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
