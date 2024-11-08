from dataclasses import dataclass

from library.application.use_case import ICommand
from library.domains.entities.user import UpdateUser, User
from library.domains.services.user import UserService


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateUserByIdCommand(ICommand[UpdateUser, User]):
    user_service: UserService

    async def execute(self, *, input_dto: UpdateUser) -> User:
        return await self.user_service.update_user_by_id(update_user=input_dto)
