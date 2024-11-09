from http import HTTPStatus

import pytest
from dirty_equals import IsDict, IsStr
from httpx import AsyncClient
from sqlalchemy import select

from library.adapters.database.tables import BookTable

API_URL = "/api/v1/books/"


@pytest.mark.parametrize(
    "json_data",
    [
        {
            "title": "Test book",
        },
        {
            "author": "Test author",
        },
        {
            "title": "Test book",
            "author": "Test author",
        },
    ],
)
async def test_create_book__incorrect_data(client: AsyncClient, json_data):
    response = await client.post(API_URL, json=json_data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_create_book__ok__status(client: AsyncClient):
    response = await client.post(
        API_URL,
        json={
            "title": "Test book",
            "author": "Test author",
            "year": 2024,
        },
    )
    assert response.status_code == HTTPStatus.CREATED


async def test_create_book__ok__format(client: AsyncClient):
    response = await client.post(
        API_URL,
        json={
            "title": "Test book",
            "author": "Test author",
            "year": 2024,
        },
    )
    assert response.json() == {
        "id": IsStr(),
        "title": "Test book",
        "author": "Test author",
        "year": 2024,
        "created_at": IsStr(),
        "updated_at": IsStr(),
    }


async def test_create_book__ok__check_db(client: AsyncClient, session):
    response = await client.post(
        API_URL,
        json={
            "title": "Test book",
            "author": "Test author",
            "year": 2024,
        },
    )
    stmt = select(BookTable).where(BookTable.id == response.json()["id"])
    db_book = (await session.scalars(stmt)).one()
    assert response.json() == IsDict(
        {
            "id": str(db_book.id),
            "title": db_book.title,
            "author": db_book.author,
            "year": db_book.year,
            "created_at": IsStr(),
            "updated_at": IsStr(),
        }
    )


async def test_create_book__duplicate_conflict(client: AsyncClient):
    book_data = {
        "title": "Test book",
        "author": "Test author",
        "year": 2024,
    }
    await client.post(
        API_URL,
        json=book_data,
    )
    response = await client.post(
        API_URL,
        json=book_data,
    )
    assert response.status_code == HTTPStatus.CONFLICT
