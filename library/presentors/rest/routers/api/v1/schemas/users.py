from collections.abc import Sequence
from datetime import datetime

from pydantic import EmailStr, Field

from library.domain.entities.user import UserId
from library.presentors.rest.schemas import BaseSchema


class UserSchema(BaseSchema):
    id: UserId
    username: str
    email: str
    created_at: datetime
    updated_at: datetime


class UserPaginationSchema(BaseSchema):
    total: int
    items: Sequence[UserSchema]


class CreateUserSchema(BaseSchema):
    username: str = Field(min_length=3, max_length=255)
    email: EmailStr = Field(min_length=3, max_length=255)


class UpdateUserSchema(BaseSchema):
    username: str | None = Field(default=None, min_length=3, max_length=255)
    email: EmailStr | None = Field(default=None, min_length=3, max_length=255)
