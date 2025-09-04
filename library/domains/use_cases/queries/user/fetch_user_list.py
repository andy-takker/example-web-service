from library.application.use_case import IQuery
from library.domains.entities.user import UserPagination, UserPaginationParams
from library.domains.services.user import UserService
from library.domains.uow import AbstractUow


class FetchUserListQuery(IQuery[UserPaginationParams, UserPagination]):
    _uow: AbstractUow
    _user_service: UserService

    def __init__(self, *, uow: AbstractUow, user_service: UserService) -> None:
        self._uow = uow
        self._user_service = user_service

    async def execute(self, *, input_dto: UserPaginationParams) -> UserPagination:
        async with self._uow:
            return await self._user_service.fetch_user_list(params=input_dto)
