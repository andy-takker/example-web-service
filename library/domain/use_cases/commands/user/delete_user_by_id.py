from library.application.use_case import ICommand
from library.domain.entities.user import UserId
from library.domain.services.user import UserService
from library.domain.uow import AbstractUow


class DeleteUserByIdCommand(ICommand[UserId, None]):
    _uow: AbstractUow
    _user_service: UserService

    def __init__(
        self,
        *,
        uow: AbstractUow,
        user_service: UserService,
    ) -> None:
        self._uow = uow
        self._user_service = user_service

    async def execute(self, *, input_dto: UserId) -> None:
        async with self._uow:
            await self._user_service.delete_user_by_id(user_id=input_dto)
