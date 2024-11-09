from collections.abc import Mapping
from http import HTTPStatus
from typing import Any
from uuid import UUID

import pytest
from dirty_equals import IsDict, IsStr
from httpx import AsyncClient

API_URL = "/api/v1/books/"

UUID_1 = UUID(int=1)
UUID_2 = UUID(int=2)


async def test_fetch_book_list__ok__status(client: AsyncClient):
    response = await client.get(API_URL)
    assert response.status_code == HTTPStatus.OK


async def test_fetch_book_list__ok__format(client: AsyncClient):
    response = await client.get(API_URL)
    assert response.json() == {
        "total": 0,
        "items": [],
    }


async def test_fetch_book_list__with_books__status(client: AsyncClient, create_book):
    await create_book(id=UUID_1)
    await create_book(id=UUID_2)
    response = await client.get(API_URL)
    assert response.status_code == HTTPStatus.OK


async def test_fetch_book_list__with_books__format(client: AsyncClient, create_book):
    book1 = await create_book(id=UUID_1)
    book2 = await create_book(id=UUID_2)
    response = await client.get(API_URL)
    assert response.json() == IsDict(
        {
            "total": 2,
            "items": [
                {
                    "id": str(UUID_1),
                    "title": book1.title,
                    "author": book1.author,
                    "year": book1.year,
                    "created_at": IsStr(),
                    "updated_at": IsStr(),
                },
                {
                    "id": str(UUID_2),
                    "title": book2.title,
                    "author": book2.author,
                    "year": book2.year,
                    "created_at": IsStr(),
                    "updated_at": IsStr(),
                },
            ],
        }
    )


async def test_fetch_book_list__with_limit(client: AsyncClient, create_book):
    book1 = await create_book(id=UUID_1)
    await create_book(id=UUID_2)
    response = await client.get(API_URL, params={"limit": 1})
    assert response.json() == IsDict(
        {
            "total": 2,
            "items": [
                {
                    "id": str(UUID_1),
                    "title": book1.title,
                    "author": book1.author,
                    "year": book1.year,
                    "created_at": IsStr(),
                    "updated_at": IsStr(),
                },
            ],
        }
    )


async def test_fetch_book_list__with_offset(client: AsyncClient, create_book):
    await create_book(id=UUID_1)
    book2 = await create_book(id=UUID_2)
    response = await client.get(API_URL, params={"offset": 1})
    assert response.json() == IsDict(
        {
            "total": 2,
            "items": [
                {
                    "id": str(UUID_2),
                    "title": book2.title,
                    "author": book2.author,
                    "year": book2.year,
                    "created_at": IsStr(),
                    "updated_at": IsStr(),
                },
            ],
        }
    )


@pytest.mark.parametrize(
    "params",
    [
        {"limit": -1},
        {"offset": -1},
        {"limit": "a"},
        {"offset": "a"},
        {"limit": 101},
    ],
)
async def test_fetch_book_list__incorrect_params(
    client: AsyncClient, params: Mapping[str, Any]
):
    response = await client.get(API_URL, params=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
