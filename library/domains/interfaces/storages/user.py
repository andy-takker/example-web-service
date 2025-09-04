from collections.abc import Sequence
from typing import Protocol

from library.domains.entities.user import (
    CreateUser,
    UpdateUser,
    User,
    UserId,
    UserPaginationParams,
)


class IUserStorage(Protocol):
    async def fetch_user_by_id(self, *, user_id: UserId) -> User | None: ...

    async def count_users(self, *, params: UserPaginationParams) -> int: ...

    async def fetch_user_list(
        self, *, params: UserPaginationParams
    ) -> Sequence[User]: ...

    async def create_user(self, *, user: CreateUser) -> User: ...

    async def delete_user_by_id(self, *, user_id: UserId) -> None: ...

    async def update_user_by_id(self, *, update_user: UpdateUser) -> User: ...

    async def exists_user_by_id(self, *, user_id: UserId) -> bool: ...
