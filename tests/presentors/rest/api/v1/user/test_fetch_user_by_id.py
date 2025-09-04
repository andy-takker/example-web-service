from http import HTTPStatus
from uuid import UUID, uuid4

from dirty_equals import IsDatetime, IsDict
from httpx import AsyncClient


def api_url(user_id: UUID | None = None) -> str:
    if user_id is None:
        user_id = uuid4()
    return f"/api/v1/users/{user_id}/"


async def test_fetch_user_by_id__not_found__status(client: AsyncClient):
    response = await client.get(api_url())
    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_fetch_user_by_id__not_found__format(client: AsyncClient):
    user_id = uuid4()
    response = await client.get(api_url(user_id))
    assert response.json() == {
        "message": f"User with id {user_id} not found",
        "ok": False,
        "status_code": HTTPStatus.NOT_FOUND,
    }


async def test_fetch_user_by_id__ok__status(
    create_db_user_factory, client: AsyncClient
):
    user = await create_db_user_factory()

    response = await client.get(api_url(user.id))
    assert response.status_code == HTTPStatus.OK


async def test_fetch_user_by_id__ok__format(
    create_db_user_factory, client: AsyncClient
):
    user = await create_db_user_factory()

    response = await client.get(api_url(user.id))
    assert response.json() == IsDict(
        {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "created_at": IsDatetime(iso_string=True),
            "updated_at": IsDatetime(iso_string=True),
        }
    )
