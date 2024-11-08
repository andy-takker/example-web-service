from collections.abc import Sequence
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, PositiveInt

from library.domains.entities.user import UserId


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UserId
    username: str
    email: str
    created_at: datetime
    updated_at: datetime


class UserPaginationParamsSchema(BaseModel):
    limit: PositiveInt = Field(le=100, default=10)
    offset: int = Field(ge=0, default=0)


class UserPaginationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total: int
    items: Sequence[UserSchema]


class CreateUserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=255)
    email: EmailStr = Field(min_length=3, max_length=255)


class UpdateUserSchema(BaseModel):
    username: str | None = Field(min_length=3, max_length=255)
    email: EmailStr | None = Field(min_length=3, max_length=255)
