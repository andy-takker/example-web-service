from http import HTTPStatus
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query

from library.application.exceptions import EmptyPayloadException
from library.domains.entities.user import (
    CreateUser,
    UpdateUser,
    UserId,
    UserPaginationParams,
)
from library.domains.uow import AbstractUow
from library.domains.use_cases.commands.user.create_user import CreateUserCommand
from library.domains.use_cases.commands.user.delete_user_by_id import (
    DeleteUserByIdCommand,
)
from library.domains.use_cases.commands.user.update_user_by_id import (
    UpdateUserByIdCommand,
)
from library.domains.use_cases.queries.user.fetch_user_by_id import FetchUserByIdQuery
from library.domains.use_cases.queries.user.fetch_user_list import FetchUserListQuery
from library.presentors.rest.routers.api.v1.schemas.users import (
    CreateUserSchema,
    UpdateUserSchema,
    UserPaginationParamsSchema,
    UserPaginationSchema,
    UserSchema,
)

router = APIRouter(prefix="/users", tags=["Users"], route_class=DishkaRoute)


@router.get(
    "/",
    response_model=UserPaginationSchema,
    status_code=HTTPStatus.OK,
    name="Get users list",
    description="Fetch users list by pagination",
)
async def fetch_users(
    params: UserPaginationParamsSchema = Query(),
    *,
    fetch_user_list: FromDishka[FetchUserListQuery],
    uow: FromDishka[AbstractUow],
) -> UserPaginationSchema:
    users = await fetch_user_list.execute(
        input_dto=UserPaginationParams(limit=params.limit, offset=params.offset)
    )
    return UserPaginationSchema.model_validate(users)


@router.post(
    "/",
    response_model=UserSchema,
    status_code=HTTPStatus.CREATED,
    name="Create user",
    description="Create new user",
)
async def create_user(
    create_user_data: CreateUserSchema,
    *,
    create_user: FromDishka[CreateUserCommand],
    uow: FromDishka[AbstractUow],
) -> UserSchema:
    user = await create_user.execute(
        input_dto=CreateUser(
            username=create_user_data.username,
            email=create_user_data.email,
        ),
    )
    return UserSchema.model_validate(user)


@router.get(
    "/{user_id}/",
    response_model=UserSchema,
    status_code=HTTPStatus.OK,
    name="Get user by ID",
    description="Fetch user by ID",
)
async def fetch_user(
    user_id: UUID,
    *,
    fetch_user_by_id: FromDishka[FetchUserByIdQuery],
    uow: FromDishka[AbstractUow],
) -> UserSchema:
    user = await fetch_user_by_id.execute(input_dto=UserId(user_id))
    return UserSchema.model_validate(user)


@router.patch(
    "/{user_id}/",
    response_model=UserSchema,
    status_code=HTTPStatus.OK,
    name="Update user by ID",
    description="Update user by ID",
)
async def update_user_by_id(
    user_id: UUID,
    update_user_data: UpdateUserSchema,
    *,
    update_user: FromDishka[UpdateUserByIdCommand],
) -> UserSchema:
    values = update_user_data.model_dump(exclude_unset=True)
    if not values:
        raise EmptyPayloadException(message="No values to update")
    user = await update_user.execute(
        input_dto=UpdateUser(
            id=UserId(user_id),
            **values,
        ),
    )
    return UserSchema.model_validate(user)


@router.delete(
    "/{user_id}/",
    status_code=HTTPStatus.NO_CONTENT,
    name="Delete user by ID",
    description="Delete user by ID",
)
async def delete_user_by_id(
    user_id: UUID,
    *,
    delete_user_by_id: FromDishka[DeleteUserByIdCommand],
    uow: FromDishka[AbstractUow],
) -> None:
    await delete_user_by_id.execute(input_dto=UserId(user_id))
