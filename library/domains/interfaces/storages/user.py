from abc import abstractmethod
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
    @abstractmethod
    async def fetch_user_by_id(self, *, user_id: UserId) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def count_users(self, *, params: UserPaginationParams) -> int:
        raise NotImplementedError

    @abstractmethod
    async def fetch_user_list(self, *, params: UserPaginationParams) -> Sequence[User]:
        raise NotImplementedError

    @abstractmethod
    async def create_user(self, *, user: CreateUser) -> User:
        raise NotImplementedError

    @abstractmethod
    async def delete_user_by_id(self, *, user_id: UserId) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user_by_id(self, *, update_user: UpdateUser) -> User:
        raise NotImplementedError

    @abstractmethod
    async def exists_user_by_id(self, *, user_id: UserId) -> bool:
        raise NotImplementedError
