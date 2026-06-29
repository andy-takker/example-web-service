from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, delete, get, patch, post
from litestar.params import Parameter

from library.application.exceptions import EmptyPayloadException
from library.domain.entities.user import (
    CreateUser,
    UpdateUser,
    UserId,
    UserPaginationParams,
)
from library.domain.use_cases.commands.user.create_user import CreateUserCommand
from library.domain.use_cases.commands.user.delete_user_by_id import (
    DeleteUserByIdCommand,
)
from library.domain.use_cases.commands.user.update_user_by_id import (
    UpdateUserByIdCommand,
)
from library.domain.use_cases.queries.user.fetch_user_by_id import FetchUserByIdQuery
from library.domain.use_cases.queries.user.fetch_user_list import FetchUserListQuery
from library.presentors.rest.routers.api.v1.schemas.users import (
    CreateUserSchema,
    UpdateUserSchema,
    UserPaginationSchema,
    UserSchema,
)


class UsersController(Controller):
    path = "/users"
    tags = ["Users"]

    @get(
        "/",
        status_code=HTTPStatus.OK,
        name="Get users list",
        description="Fetch users list by pagination",
    )
    @inject
    async def fetch_users(
        self,
        fetch_user_list: FromDishka[FetchUserListQuery],
        limit: Annotated[int, Parameter(ge=1, le=100)] = 10,
        offset: Annotated[int, Parameter(ge=0)] = 0,
    ) -> UserPaginationSchema:
        users = await fetch_user_list.execute(
            input_dto=UserPaginationParams(limit=limit, offset=offset)
        )
        return UserPaginationSchema.model_validate(users)

    @post(
        "/",
        status_code=HTTPStatus.CREATED,
        name="Create user",
        description="Create new user",
    )
    @inject
    async def create_user(
        self,
        data: CreateUserSchema,
        create_user: FromDishka[CreateUserCommand],
    ) -> UserSchema:
        user = await create_user.execute(
            input_dto=CreateUser(
                username=data.username,
                email=data.email,
            ),
        )
        return UserSchema.model_validate(user)

    @get(
        "/{user_id:uuid}/",
        status_code=HTTPStatus.OK,
        name="Get user by ID",
        description="Fetch user by ID",
    )
    @inject
    async def fetch_user(
        self,
        user_id: UUID,
        fetch_user_by_id: FromDishka[FetchUserByIdQuery],
    ) -> UserSchema:
        user = await fetch_user_by_id.execute(input_dto=UserId(user_id))
        return UserSchema.model_validate(user)

    @patch(
        "/{user_id:uuid}/",
        status_code=HTTPStatus.OK,
        name="Update user by ID",
        description="Update user by ID",
    )
    @inject
    async def update_user_by_id(
        self,
        update_user: FromDishka[UpdateUserByIdCommand],
        user_id: UUID,
        data: UpdateUserSchema,
    ) -> UserSchema:
        values = data.model_dump(exclude_unset=True)
        if not values:
            raise EmptyPayloadException(message="No values to update")
        user = await update_user.execute(
            input_dto=UpdateUser(
                id=UserId(user_id),
                **values,
            ),
        )
        return UserSchema.model_validate(user)

    @delete(
        "/{user_id:uuid}/",
        status_code=HTTPStatus.NO_CONTENT,
        name="Delete user by ID",
        description="Delete user by ID",
    )
    @inject
    async def delete_user_by_id(
        self,
        delete_user_by_id: FromDishka[DeleteUserByIdCommand],
        user_id: UUID,
    ) -> None:
        await delete_user_by_id.execute(input_dto=UserId(user_id))
