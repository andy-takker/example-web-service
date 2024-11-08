from library.application.use_case import IQuery
from library.domains.entities.user import User, UserId
from library.domains.services.user import UserService


class FetchUserByIdQuery(IQuery[UserId, User]):
    __user_service: UserService

    def __init__(self, user_service: UserService) -> None:
        self.__user_service = user_service

    async def execute(self, *, input_dto: UserId) -> User:
        return await self.__user_service.fetch_user_by_id(user_id=input_dto)
