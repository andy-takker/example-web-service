from dataclasses import dataclass

from library.application.use_case import ICommand
from library.domains.entities.user import CreateUser, User
from library.domains.services.user import UserService
from library.domains.uow import AbstractUow


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateUserCommand(ICommand[CreateUser, User]):
    user_service: UserService
    uow: AbstractUow

    async def execute(self, *, input_dto: CreateUser) -> User:
        async with self.uow:
            return await self.user_service.create_user(user=input_dto)
