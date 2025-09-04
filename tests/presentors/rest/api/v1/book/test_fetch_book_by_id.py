from http import HTTPStatus
from uuid import UUID, uuid4

from dirty_equals import IsDatetime, IsDict
from httpx import AsyncClient


def api_url(book_id: UUID | None = None) -> str:
    if book_id is None:
        book_id = uuid4()
    return f"/api/v1/books/{book_id}/"


async def test_fetch_book_by_id__not_found__status(client: AsyncClient):
    response = await client.get(api_url())
    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_fetch_book_by_id__not_found__format(client: AsyncClient):
    book_id = uuid4()
    response = await client.get(api_url(book_id))
    assert response.json() == {
        "message": f"Book with id {book_id} not found",
        "ok": False,
        "status_code": HTTPStatus.NOT_FOUND,
    }


async def test_fetch_book_by_id__ok__status(create_book, client: AsyncClient):
    book = await create_book()

    response = await client.get(api_url(book_id=book.id))
    assert response.status_code == HTTPStatus.OK


async def test_fetch_book_by_id__ok__format(create_book, client: AsyncClient):
    book = await create_book()

    response = await client.get(api_url(book_id=book.id))
    assert response.json() == IsDict(
        {
            "id": str(book.id),
            "title": book.title,
            "year": book.year,
            "author": book.author,
            "created_at": IsDatetime(iso_string=True),
            "updated_at": IsDatetime(iso_string=True),
        }
    )
