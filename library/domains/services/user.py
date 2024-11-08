from library.application.exceptions import EntityNotFoundException
from library.domains.entities.user import (
    CreateUser,
    UpdateUser,
    User,
    UserId,
    UserPagination,
    UserPaginationParams,
)
from library.domains.interfaces.storages.user import IUserStorage


class UserService:
    __user_storage: IUserStorage

    def __init__(self, user_storage: IUserStorage) -> None:
        self.__user_storage = user_storage

    async def fetch_user_by_id(self, *, user_id: UserId) -> User:
        user = await self.__user_storage.fetch_user_by_id(user_id=user_id)
        if user is None:
            raise EntityNotFoundException(entity=User, entity_id=user_id)
        return user

    async def fetch_user_list(self, *, params: UserPaginationParams) -> UserPagination:
        total = await self.__user_storage.count_users(params=params)
        items = await self.__user_storage.fetch_user_list(params=params)
        return UserPagination(total=total, items=items)

    async def create_user(self, *, user: CreateUser) -> User:
        return await self.__user_storage.create_user(user=user)

    async def delete_user_by_id(self, *, user_id: UserId) -> None:
        if not await self.__user_storage.exists_user_by_id(user_id=user_id):
            raise EntityNotFoundException(entity=User, entity_id=user_id)
        await self.__user_storage.delete_user_by_id(user_id=user_id)

    async def update_user_by_id(self, *, update_user: UpdateUser) -> User:
        if not await self.__user_storage.exists_user_by_id(user_id=update_user.id):
            raise EntityNotFoundException(entity=User, entity_id=update_user.id)
        return await self.__user_storage.update_user_by_id(update_user=update_user)
