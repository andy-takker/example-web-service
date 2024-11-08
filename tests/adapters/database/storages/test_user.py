from datetime import UTC, datetime
from uuid import UUID

import pytest
from sqlalchemy import select

from library.adapters.database.tables import UserTable
from library.application.exceptions import (
    EntityNotFoundException,
    UserAlreadyExistsException,
)
from library.domains.entities.user import (
    CreateUser,
    UpdateUser,
    User,
    UserId,
    UserPaginationParams,
)
from library.domains.interfaces.storages.user import IUserStorage

UUID_1 = UUID(int=1)
UUID_2 = UUID(int=2)


async def test_fetch_user_by_id__not_found(user_storage: IUserStorage):
    assert await user_storage.fetch_user_by_id(user_id=UserId(UUID_1)) is None


async def test_fetch_user_by_id__was_deleted(user_storage: IUserStorage, create_user):
    await create_user(id=UUID_1, deleted_at=datetime.now(tz=UTC))
    assert await user_storage.fetch_user_by_id(user_id=UserId(UUID_1)) is None


async def test_fetch_user_by_id__ok(user_storage: IUserStorage, create_user):
    user = await create_user(id=UUID_1)
    storage_user = await user_storage.fetch_user_by_id(user_id=UserId(UUID_1))
    assert storage_user == User(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


async def test_exists_user_by_id__not_found(user_storage: IUserStorage):
    assert await user_storage.exists_user_by_id(user_id=UserId(UUID_1)) is False


async def test_exists_user_by_id__was_deleted(user_storage: IUserStorage, create_user):
    await create_user(id=UUID_1, deleted_at=datetime.now(tz=UTC))
    assert await user_storage.exists_user_by_id(user_id=UserId(UUID_1)) is False


async def test_exists_user_by_id__ok(user_storage: IUserStorage, create_user):
    await create_user(id=UUID_1)
    assert await user_storage.exists_user_by_id(user_id=UserId(UUID_1))


async def test_fetch_user_list__ok(user_storage: IUserStorage, create_user):
    users = [
        await create_user(id=UUID_1),
        await create_user(id=UUID_2),
    ]
    db_users = await user_storage.fetch_user_list(
        params=UserPaginationParams(limit=10, offset=0)
    )
    assert db_users == [
        User(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        for user in users
    ]


async def test_user_list__with_offset(user_storage: IUserStorage, create_user):
    await create_user(id=UUID_1)
    user = await create_user(id=UUID_2)
    assert await user_storage.fetch_user_list(
        params=UserPaginationParams(limit=10, offset=1)
    ) == [
        User(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
    ]


async def test_user_list__with_limit(user_storage: IUserStorage, create_user):
    user = await create_user(id=UUID_1)
    await create_user(id=UUID_2)
    assert await user_storage.fetch_user_list(
        params=UserPaginationParams(limit=1, offset=0)
    ) == [
        User(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
    ]


async def test_count_users__ok(user_storage: IUserStorage, create_user):
    await create_user(id=UUID_1)
    await create_user(id=UUID_2)
    assert (
        await user_storage.count_users(params=UserPaginationParams(limit=10, offset=0))
        == 2
    )


async def test_create_user__ok(user_storage: IUserStorage, session):
    user = await user_storage.create_user(
        user=CreateUser(
            username="username",
            email="email@example.com",
        )
    )

    stmt = select(UserTable).where(UserTable.id == user.id)
    db_user = (await session.scalars(stmt)).first()
    assert user == User(
        id=UserId(db_user.id),
        username=db_user.username,
        email=db_user.email,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
    )


async def test_create_user__duplicate_username(user_storage: IUserStorage, create_user):
    await create_user(id=UUID_1, username="username")
    with pytest.raises(UserAlreadyExistsException):
        await user_storage.create_user(
            user=CreateUser(
                username="username",
                email="email@example.com",
            )
        )


async def test_create_user__duplicate_email(user_storage: IUserStorage, create_user):
    await create_user(id=UUID_1, email="email@example.com")
    with pytest.raises(UserAlreadyExistsException):
        await user_storage.create_user(
            user=CreateUser(
                username="username",
                email="email@example.com",
            )
        )


async def test_delete_user_by_id__ok(user_storage: IUserStorage, create_user, session):
    user = await create_user(id=UUID_1)
    await user_storage.delete_user_by_id(user_id=user.id)

    stmt = select(UserTable).where(UserTable.id == user.id)
    user = (await session.scalars(stmt)).first()
    assert user.deleted_at is not None


async def test_delete_user_by_id__not_found(user_storage: IUserStorage):
    assert await user_storage.delete_user_by_id(user_id=UserId(UUID_1)) is None


async def test_update_user_by_id__ok(user_storage: IUserStorage, create_user, session):
    user = await create_user(id=UUID_1, username="old_username")
    await user_storage.update_user_by_id(
        update_user=UpdateUser(
            id=user.id,
            username="new_username",
        )
    )
    stmt = select(UserTable).where(UserTable.id == user.id)
    user = (await session.scalars(stmt)).first()
    assert user.username == "new_username"


async def test_update_user_by_id__not_found(user_storage: IUserStorage):
    with pytest.raises(EntityNotFoundException):
        await user_storage.update_user_by_id(
            update_user=UpdateUser(id=UserId(UUID_1), username="new_username")
        ) is None
