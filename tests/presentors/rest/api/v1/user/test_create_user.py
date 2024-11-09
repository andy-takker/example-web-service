from http import HTTPStatus

import pytest
from dirty_equals import IsDict, IsStr
from httpx import AsyncClient
from sqlalchemy import select

from library.adapters.database.tables import UserTable

API_URL = "/api/v1/users/"


@pytest.mark.parametrize(
    "json_data",
    [
        {
            "username": "onlyusername",
        },
        {
            "email": "only@email.com",
        },
        {
            "email": "incorrect@email",
        },
    ],
)
async def test_create_user__incorrect_data(client: AsyncClient, json_data):
    response = await client.post(API_URL, json=json_data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_create_user__ok__status(client: AsyncClient):
    response = await client.post(
        API_URL,
        json={
            "username": "username",
            "email": "email@example.com",
        },
    )
    assert response.status_code == HTTPStatus.CREATED


async def test_create_user__ok__format(client: AsyncClient):
    response = await client.post(
        API_URL,
        json={
            "username": "username",
            "email": "email@example.com",
        },
    )
    assert response.json() == {
        "id": IsStr(),
        "username": "username",
        "email": "email@example.com",
        "created_at": IsStr(),
        "updated_at": IsStr(),
    }


async def test_create_user__ok__check_db(client: AsyncClient, session):
    response = await client.post(
        API_URL,
        json={
            "username": "username",
            "email": "email@example.com",
        },
    )
    stmt = select(UserTable).where(UserTable.id == response.json()["id"])
    db_user = (await session.scalars(stmt)).one()
    assert response.json() == IsDict(
        {
            "id": str(db_user.id),
            "username": db_user.username,
            "email": db_user.email,
            "created_at": IsStr(),
            "updated_at": IsStr(),
        }
    )


async def test_create_user__duplicate_email__conflict(client: AsyncClient):
    await client.post(
        API_URL,
        json={
            "username": "username1",
            "email": "email@example.com",
        },
    )
    response = await client.post(
        API_URL,
        json={
            "username": "username2",
            "email": "email@example.com",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT


async def test_create_user__duplicate_username__conflict(client: AsyncClient):
    await client.post(
        API_URL,
        json={
            "username": "username",
            "email": "email1@example.com",
        },
    )
    response = await client.post(
        API_URL,
        json={
            "username": "username",
            "email": "email2@example.com",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
