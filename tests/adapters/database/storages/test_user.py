from datetime import UTC, datetime
from uuid import UUID

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from library.adapters.database.storages.user import UserStorage
from library.adapters.database.tables import UserTable
from library.adapters.database.uow import SqlalchemyUow
from library.application.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)
from library.domains.entities.user import (
    CreateUser,
    UpdateUser,
    User,
    UserId,
    UserPaginationParams,
)

UUID_1 = UUID(int=1)
UUID_2 = UUID(int=2)


async def test_fetch_user_by_id__not_found(
    uow: SqlalchemyUow, user_storage: UserStorage
):
    async with uow:
        assert await user_storage.fetch_user_by_id(user_id=UserId(UUID_1)) is None


async def test_fetch_user_by_id__was_deleted(
    uow: SqlalchemyUow, user_storage: UserStorage, create_db_user_factory
):
    await create_db_user_factory(id=UUID_1, deleted_at=datetime.now(tz=UTC))
    async with uow:
        assert await user_storage.fetch_user_by_id(user_id=UserId(UUID_1)) is None


async def test_fetch_user_by_id__ok(
    uow: SqlalchemyUow, user_storage: UserStorage, create_db_user_factory
):
    user = await create_db_user_factory(id=UUID_1)
    async with uow:
        storage_user = await user_storage.fetch_user_by_id(user_id=UserId(UUID_1))
    assert storage_user == User(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


async def test_exists_user_by_id__not_found(
    uow: SqlalchemyUow, user_storage: UserStorage
):
    async with uow:
        assert await user_storage.exists_user_by_id(user_id=UserId(UUID_1)) is False


async def test_exists_user_by_id__was_deleted(
    uow: SqlalchemyUow, user_storage: UserStorage, create_db_user_factory
):
    await create_db_user_factory(id=UUID_1, deleted_at=datetime.now(tz=UTC))
    async with uow:
        assert await user_storage.exists_user_by_id(user_id=UserId(UUID_1)) is False


async def test_exists_user_by_id__ok(
    uow: SqlalchemyUow, user_storage: UserStorage, create_db_user_factory
):
    await create_db_user_factory(id=UUID_1)
    async with uow:
        assert await user_storage.exists_user_by_id(user_id=UserId(UUID_1))


async def test_fetch_user_list__ok(
    uow: SqlalchemyUow, user_storage: UserStorage, create_db_user_factory
):
    users = [
        await create_db_user_factory(id=UUID_1),
        await create_db_user_factory(id=UUID_2),
    ]
    async with uow:
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


async def test_user_list__with_offset(
    uow: SqlalchemyUow, user_storage: UserStorage, create_db_user_factory
):
    await create_db_user_factory(id=UUID_1)
    user = await create_db_user_factory(id=UUID_2)
    async with uow:
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


async def test_user_list__with_limit(
    uow: SqlalchemyUow, user_storage: UserStorage, create_db_user_factory
):
    user = await create_db_user_factory(id=UUID_1)
    await create_db_user_factory(id=UUID_2)
    async with uow:
        users = await user_storage.fetch_user_list(
            params=UserPaginationParams(limit=1, offset=0)
        )
    assert users == [
        User(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
    ]


async def test_count_users__ok(
    uow: SqlalchemyUow, user_storage: UserStorage, create_db_user_factory
):
    await create_db_user_factory(id=UUID_1)
    await create_db_user_factory(id=UUID_2)
    async with uow:
        count = await user_storage.count_users(
            params=UserPaginationParams(limit=10, offset=0)
        )
    assert count == 2


async def test_create_user__ok(
    uow: SqlalchemyUow, user_storage: UserStorage, session: AsyncSession
):
    async with uow:
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


async def test_create_user__duplicate_username(
    uow: SqlalchemyUow, user_storage: UserStorage, create_db_user_factory
):
    await create_db_user_factory(id=UUID_1, username="username")
    with pytest.raises(EntityAlreadyExistsException):
        async with uow:
            await user_storage.create_user(
                user=CreateUser(
                    username="username",
                    email="email@example.com",
                )
            )


async def test_create_user__duplicate_email(
    uow: SqlalchemyUow, user_storage: UserStorage, create_db_user_factory
):
    await create_db_user_factory(id=UUID_1, email="email@example.com")
    with pytest.raises(EntityAlreadyExistsException):
        async with uow:
            await user_storage.create_user(
                user=CreateUser(
                    username="username",
                    email="email@example.com",
                )
            )


async def test_delete_user_by_id__ok(
    uow: SqlalchemyUow,
    user_storage: UserStorage,
    create_db_user_factory,
    session: AsyncSession,
):
    user = await create_db_user_factory(id=UUID_1)
    async with uow:
        await user_storage.delete_user_by_id(user_id=user.id)

    stmt = select(UserTable.deleted_at).where(UserTable.id == user.id)
    user_deleted_at = await session.scalar(stmt)
    assert user_deleted_at is not None


async def test_delete_user_by_id__not_found(
    uow: SqlalchemyUow, user_storage: UserStorage
):
    async with uow:
        assert await user_storage.delete_user_by_id(user_id=UserId(UUID_1)) is None


async def test_update_user_by_id__ok(
    uow: SqlalchemyUow,
    user_storage: UserStorage,
    create_db_user_factory,
    session: AsyncSession,
):
    user = await create_db_user_factory(id=UUID_1, username="old_username")
    async with uow:
        await user_storage.update_user_by_id(
            update_user=UpdateUser(
                id=user.id,
                username="new_username",
            )
        )
    stmt = select(UserTable.username).where(UserTable.id == user.id)
    user_username = await session.scalar(stmt)
    assert user_username == "new_username"


async def test_update_user_by_id__not_found(
    uow: SqlalchemyUow, user_storage: UserStorage
):
    with pytest.raises(EntityNotFoundException):
        async with uow:
            assert (
                await user_storage.update_user_by_id(
                    update_user=UpdateUser(id=UserId(UUID_1), username="new_username")
                )
                is None
            )
