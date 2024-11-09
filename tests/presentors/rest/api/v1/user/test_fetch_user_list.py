from collections.abc import Mapping
from http import HTTPStatus
from typing import Any
from uuid import UUID

import pytest
from dirty_equals import IsDict, IsStr
from httpx import AsyncClient

API_URL = "/api/v1/users/"

UUID_1 = UUID(int=1)
UUID_2 = UUID(int=2)


async def test_fetch_user_list__ok__status(client: AsyncClient):
    response = await client.get(API_URL)
    assert response.status_code == HTTPStatus.OK


async def test_fetch_user_list__ok__format(client: AsyncClient):
    response = await client.get(API_URL)
    assert response.json() == {
        "total": 0,
        "items": [],
    }


async def test_fetch_user_list__with_users__status(client: AsyncClient, create_user):
    await create_user(id=UUID_1)
    await create_user(id=UUID_2)
    response = await client.get(API_URL)
    assert response.status_code == HTTPStatus.OK


async def test_fetch_user_list__with_users__format(client: AsyncClient, create_user):
    user1 = await create_user(id=UUID_1)
    user2 = await create_user(id=UUID_2)
    response = await client.get(API_URL)
    assert response.json() == IsDict(
        {
            "total": 2,
            "items": [
                {
                    "id": str(UUID_1),
                    "username": user1.username,
                    "email": user1.email,
                    "created_at": IsStr(),
                    "updated_at": IsStr(),
                },
                {
                    "id": str(UUID_2),
                    "username": user2.username,
                    "email": user2.email,
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
async def test_fetch_user_list__incorrect_params(
    client: AsyncClient, params: Mapping[str, Any]
):
    response = await client.get(API_URL, params=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_fetch_user_list__with_limit(client: AsyncClient, create_user):
    user1 = await create_user(id=UUID_1)
    await create_user(id=UUID_2)
    response = await client.get(API_URL, params={"limit": 1})
    assert response.json() == IsDict(
        {
            "total": 2,
            "items": [
                {
                    "id": str(UUID_1),
                    "username": user1.username,
                    "email": user1.email,
                    "created_at": IsStr(),
                    "updated_at": IsStr(),
                },
            ],
        }
    )


async def test_fetch_user_list__with_offset(client: AsyncClient, create_user):
    await create_user(id=UUID_1)
    user2 = await create_user(id=UUID_2)
    response = await client.get(API_URL, params={"offset": 1})
    assert response.json() == IsDict(
        {
            "total": 2,
            "items": [
                {
                    "id": str(UUID_2),
                    "username": user2.username,
                    "email": user2.email,
                    "created_at": IsStr(),
                    "updated_at": IsStr(),
                },
            ],
        }
    )
