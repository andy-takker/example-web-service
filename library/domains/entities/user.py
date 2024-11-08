from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from uuid import UUID

from library.application.entities import UNSET, Unset

UserId = NewType("UserId", UUID)


@dataclass(frozen=True, kw_only=True, slots=True)
class User:
    id: UserId
    username: str
    email: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class UserPaginationParams:
    limit: int
    offset: int


@dataclass(frozen=True, kw_only=True, slots=True)
class UserPagination:
    total: int
    items: Sequence[User]


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateUser:
    username: str
    email: str


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateUser:
    id: UserId
    username: str | Unset = UNSET
    email: str | Unset = UNSET

    def to_dict(self) -> Mapping[str, int | str]:
        values: dict[str, int | str] = {}
        if not isinstance(self.username, Unset):
            values["username"] = self.username
        if not isinstance(self.email, Unset):
            values["email"] = self.email
        return values
