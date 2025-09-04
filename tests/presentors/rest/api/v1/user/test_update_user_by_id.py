from http import HTTPStatus
from uuid import UUID, uuid4

from dirty_equals import IsDatetime, IsDict
from httpx import AsyncClient


def api_url(user_id: UUID | None = None) -> str:
    if user_id is None:
        user_id = uuid4()
    return f"/api/v1/users/{user_id}/"


async def test_update_user_by_id__nothing_to_update__status_code(client: AsyncClient):
    response = await client.patch(api_url())
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_update_user_by_id__nothing_to_update__format(client: AsyncClient):
    response = await client.patch(api_url(), json={})
    assert response.json() == {
        "message": "No values to update",
        "ok": False,
        "status_code": HTTPStatus.BAD_REQUEST,
    }


async def test_update_user_by_id__not_found__status_code(client: AsyncClient):
    response = await client.patch(api_url(uuid4()), json={"username": "new_username"})
    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_update_user_by_id__not_found__format(client: AsyncClient):
    user_id = uuid4()
    response = await client.patch(api_url(user_id), json={"username": "new_username"})
    assert response.json() == {
        "message": f"User with id {user_id} not found",
        "ok": False,
        "status_code": HTTPStatus.NOT_FOUND,
    }


async def test_update_user_by_id__ok__status(
    client: AsyncClient, create_db_user_factory
):
    user = await create_db_user_factory()
    response = await client.patch(api_url(user.id), json={"username": "new_username"})
    assert response.status_code == HTTPStatus.OK


async def test_update_user_by_id__ok__format(
    client: AsyncClient, create_db_user_factory
):
    user = await create_db_user_factory()
    response = await client.patch(api_url(user.id), json={"username": "new_username"})
    assert response.json() == IsDict(
        {
            "id": str(user.id),
            "username": "new_username",
            "email": user.email,
            "created_at": IsDatetime(iso_string=True),
            "updated_at": IsDatetime(iso_string=True),
        }
    )
