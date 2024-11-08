from dataclasses import dataclass

from library.application.use_case import ICommand
from library.domains.entities.user import UserId
from library.domains.services.user import UserService


@dataclass(frozen=True, kw_only=True, slots=True)
class DeleteUserByIdCommand(ICommand[UserId, None]):
    user_service: UserService

    async def execute(self, *, input_dto: UserId) -> None:
        await self.user_service.delete_user_by_id(user_id=input_dto)
