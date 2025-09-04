from http import HTTPStatus
from uuid import UUID

from httpx import AsyncClient
from sqlalchemy import select

from library.adapters.database.tables import UserTable

UUID_1 = UUID(int=1)


def api_url(user_id: UUID) -> str:
    return f"/api/v1/users/{user_id}/"


async def test_delete_user_by_id__ok(create_db_user_factory, client: AsyncClient):
    await create_db_user_factory(id=UUID_1)

    response = await client.delete(api_url(user_id=UUID_1))
    assert response.status_code == HTTPStatus.NO_CONTENT


async def test_delete_user_by_id__ok__check_db(
    client: AsyncClient, session, create_db_user_factory
):
    await create_db_user_factory(id=UUID_1)
    await client.delete(api_url(user_id=UUID_1))
    stmt = select(UserTable).where(UserTable.id == UUID_1)
    user = (await session.scalars(stmt)).one()
    assert user.deleted_at


async def test_delete_user_by_id__not_found(client: AsyncClient):
    response = await client.delete(api_url(user_id=UUID_1))
    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_delete_user_by_id__double_delete__not_found(
    client: AsyncClient, create_db_user_factory
):
    await create_db_user_factory(id=UUID_1)
    await client.delete(api_url(user_id=UUID_1))
    response = await client.delete(api_url(user_id=UUID_1))
    assert response.status_code == HTTPStatus.NOT_FOUND
