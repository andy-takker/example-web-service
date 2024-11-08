from library.application.use_case import IQuery
from library.domains.entities.user import UserPagination, UserPaginationParams
from library.domains.services.user import UserService


class FetchUserListQuery(IQuery[UserPaginationParams, UserPagination]):
    __user_service: UserService

    def __init__(self, *, user_service: UserService) -> None:
        self.__user_service = user_service

    async def execute(self, *, input_dto: UserPaginationParams) -> UserPagination:
        return await self.__user_service.fetch_user_list(params=input_dto)
