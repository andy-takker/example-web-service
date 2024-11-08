from http import HTTPStatus
from uuid import UUID

from dirty_equals import IsPartialDict, IsStr
from httpx import AsyncClient

UUID_1 = UUID("00000000-0000-0000-0000-000000000001")


def api_url(book_id: UUID) -> str:
    return f"/api/v1/books/{book_id}/"


async def test_fetch_book_by_id__not_found__status(client: AsyncClient):
    response = await client.get(api_url(book_id=UUID_1))
    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_fetch_book_by_id__not_found__format(client: AsyncClient):
    response = await client.get(api_url(book_id=UUID_1))
    assert response.json() == {
        "message": f"Book with id {UUID_1} not found",
        "ok": False,
        "status_code": 404,
    }


async def test_fetch_book_by_id__ok__status(create_book, client: AsyncClient):
    await create_book(id=UUID_1)

    response = await client.get(api_url(book_id=UUID_1))
    assert response.status_code == HTTPStatus.OK


async def test_fetch_book_by_id__ok__format(create_book, client: AsyncClient):
    book = await create_book(id=UUID_1)

    response = await client.get(api_url(book_id=UUID_1))
    assert response.json() == IsPartialDict(
        {
            "id": str(UUID_1),
            "title": book.title,
            "year": book.year,
            "author": book.author,
            "created_at": IsStr(),
            "updated_at": IsStr(),
        }
    )
