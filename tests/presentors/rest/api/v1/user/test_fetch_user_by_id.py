from http import HTTPStatus
from uuid import UUID

from dirty_equals import IsDict, IsStr
from httpx import AsyncClient

UUID_1 = UUID(int=1)


def api_url(user_id: UUID) -> str:
    return f"/api/v1/users/{user_id}/"


async def test_fetch_user_by_id__not_found__status(client: AsyncClient):
    response = await client.get(api_url(user_id=UUID_1))
    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_fetch_user_by_id__not_found__format(client: AsyncClient):
    response = await client.get(api_url(user_id=UUID_1))
    assert response.json() == {
        "message": f"User with id {UUID_1} not found",
        "ok": False,
        "status_code": HTTPStatus.NOT_FOUND,
    }


async def test_fetch_user_by_id__ok__status(create_user, client: AsyncClient):
    await create_user(id=UUID_1)

    response = await client.get(api_url(user_id=UUID_1))
    assert response.status_code == HTTPStatus.OK


async def test_fetch_user_by_id__ok__format(create_user, client: AsyncClient):
    user = await create_user(id=UUID_1)

    response = await client.get(api_url(user_id=UUID_1))
    assert response.json() == IsDict(
        {
            "id": str(UUID_1),
            "username": user.username,
            "email": user.email,
            "created_at": IsStr(),
            "updated_at": IsStr(),
        }
    )
