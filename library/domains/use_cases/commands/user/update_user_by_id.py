from library.application.use_case import ICommand
from library.domains.entities.user import UpdateUser, User
from library.domains.services.user import UserService
from library.domains.uow import AbstractUow


class UpdateUserByIdCommand(ICommand[UpdateUser, User]):
    _uow: AbstractUow
    _user_service: UserService

    def __init__(self, *, uow: AbstractUow, user_service: UserService) -> None:
        self._uow = uow
        self._user_service = user_service

    async def execute(self, *, input_dto: UpdateUser) -> User:
        async with self._uow:
            return await self._user_service.update_user_by_id(update_user=input_dto)
