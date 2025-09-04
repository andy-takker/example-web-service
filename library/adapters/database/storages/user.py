from collections.abc import Sequence
from datetime import UTC, datetime
from typing import NoReturn

from sqlalchemy import exists, func, insert, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from library.adapters.database.tables import UserTable
from library.adapters.database.uow import SqlalchemyUow
from library.application.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
    LibraryException,
)
from library.domains.entities.user import (
    CreateUser,
    UpdateUser,
    User,
    UserId,
    UserPaginationParams,
)


class UserStorage:
    def __init__(self, *, uow: SqlalchemyUow) -> None:
        self._uow = uow

    @property
    def _session(self) -> AsyncSession:
        return self._uow.session

    async def fetch_user_by_id(self, *, user_id: UserId) -> User | None:
        stmt = select(UserTable).where(
            UserTable.id == user_id, UserTable.deleted_at.is_(None)
        )
        user = (await self._session.scalars(stmt)).first()
        if user is None:
            return None
        return User(
            id=UserId(user.id),
            email=user.email,
            username=user.username,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def exists_user_by_id(self, *, user_id: UserId) -> bool:
        stmt = select(
            exists().where(UserTable.id == user_id, UserTable.deleted_at.is_(None))
        )
        return bool((await self._session.execute(stmt)).scalar())

    async def count_users(self, *, params: UserPaginationParams) -> int:
        query = (
            select(func.count())
            .select_from(UserTable)
            .where(UserTable.deleted_at.is_(None))
        )
        result = (await self._session.execute(query)).scalar()
        return result or 0

    async def fetch_user_list(self, *, params: UserPaginationParams) -> Sequence[User]:
        query = (
            select(
                UserTable.id,
                UserTable.email,
                UserTable.username,
                UserTable.created_at,
                UserTable.updated_at,
            )
            .where(UserTable.deleted_at.is_(None))
            .limit(params.limit)
            .offset(params.offset)
        )
        result = (await self._session.execute(query)).mappings().all()
        return [
            User(
                id=UserId(result["id"]),
                email=result["email"],
                username=result["username"],
                created_at=result["created_at"],
                updated_at=result["updated_at"],
            )
            for result in result
        ]

    async def create_user(self, *, user: CreateUser) -> User:
        stmt = (
            insert(UserTable)
            .values(
                email=user.email,
                username=user.username,
            )
            .returning(
                UserTable.id,
                UserTable.email,
                UserTable.username,
                UserTable.created_at,
                UserTable.updated_at,
            )
        )
        try:
            result = (await self._session.execute(stmt)).mappings().one()
        except IntegrityError as e:
            self._raise_error(e)
        return User(
            id=UserId(result["id"]),
            email=result["email"],
            username=result["username"],
            created_at=result["created_at"],
            updated_at=result["updated_at"],
        )

    async def delete_user_by_id(self, *, user_id: UserId) -> None:
        stmt = (
            update(UserTable)
            .where(UserTable.id == user_id)
            .values(deleted_at=datetime.now(tz=UTC))
        )
        await self._session.execute(stmt)

    async def update_user_by_id(self, *, update_user: UpdateUser) -> User:
        stmt = (
            update(UserTable)
            .where(UserTable.id == update_user.id)
            .values(**update_user.to_dict())
            .returning(
                UserTable.id,
                UserTable.email,
                UserTable.username,
                UserTable.created_at,
                UserTable.updated_at,
            )
        )
        try:
            result = (await self._session.execute(stmt)).mappings().one()
        except NoResultFound as e:
            raise EntityNotFoundException(entity=User, entity_id=update_user.id) from e
        return User(
            id=UserId(result["id"]),
            email=result["email"],
            username=result["username"],
            created_at=result["created_at"],
            updated_at=result["updated_at"],
        )

    def _raise_error(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]

        if constraint in ("uq__users__username", "uq__users__email"):
            raise EntityAlreadyExistsException(message="User already exists") from e

        raise LibraryException(message="Unknown error") from e
