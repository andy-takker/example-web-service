from dishka import Provider, Scope, provide

from library.domains.interfaces.storages.book import IBookStorage
from library.domains.interfaces.storages.user import IUserStorage
from library.domains.services.book import BookService
from library.domains.services.user import UserService
from library.domains.use_cases.commands.book.create_book import CreateBookCommand
from library.domains.use_cases.commands.book.delete_book_by_id import (
    DeleteBookByIdCommand,
)
from library.domains.use_cases.commands.book.update_book_by_id import (
    UpdateBookByIdCommand,
)
from library.domains.use_cases.commands.user.create_user import CreateUserCommand
from library.domains.use_cases.commands.user.delete_user_by_id import (
    DeleteUserByIdCommand,
)
from library.domains.use_cases.commands.user.update_user_by_id import (
    UpdateUserByIdCommand,
)
from library.domains.use_cases.queries.book.fetch_book_by_id import FetchBookByIdQuery
from library.domains.use_cases.queries.book.fetch_book_list import FetchBookListQuery
from library.domains.use_cases.queries.user.fetch_user_by_id import FetchUserByIdQuery
from library.domains.use_cases.queries.user.fetch_user_list import FetchUserListQuery


class DomainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def book_service(self, book_storage: IBookStorage) -> BookService:
        return BookService(book_storage=book_storage)

    @provide(scope=Scope.REQUEST)
    def fetch_book_by_id(self, book_service: BookService) -> FetchBookByIdQuery:
        return FetchBookByIdQuery(book_service=book_service)

    @provide(scope=Scope.REQUEST)
    def fetch_book_list(self, book_service: BookService) -> FetchBookListQuery:
        return FetchBookListQuery(book_service=book_service)

    @provide(scope=Scope.REQUEST)
    def create_book_command(self, book_service: BookService) -> CreateBookCommand:
        return CreateBookCommand(book_service=book_service)

    @provide(scope=Scope.REQUEST)
    def delete_book_by_id_command(
        self, book_service: BookService
    ) -> DeleteBookByIdCommand:
        return DeleteBookByIdCommand(book_service=book_service)

    @provide(scope=Scope.REQUEST)
    def update_book_by_id_command(
        self, book_service: BookService
    ) -> UpdateBookByIdCommand:
        return UpdateBookByIdCommand(book_service=book_service)

    @provide(scope=Scope.REQUEST)
    def user_service(self, user_storage: IUserStorage) -> UserService:
        return UserService(user_storage=user_storage)

    @provide(scope=Scope.REQUEST)
    def fetch_user_by_id(self, user_service: UserService) -> FetchUserByIdQuery:
        return FetchUserByIdQuery(user_service=user_service)

    @provide(scope=Scope.REQUEST)
    def fetch_user_list(self, user_service: UserService) -> FetchUserListQuery:
        return FetchUserListQuery(user_service=user_service)

    @provide(scope=Scope.REQUEST)
    def create_user_command(self, user_service: UserService) -> CreateUserCommand:
        return CreateUserCommand(user_service=user_service)

    @provide(scope=Scope.REQUEST)
    def delete_user_by_id_command(
        self, user_service: UserService
    ) -> DeleteUserByIdCommand:
        return DeleteUserByIdCommand(user_service=user_service)

    @provide(scope=Scope.REQUEST)
    def update_user_by_id_command(
        self, user_service: UserService
    ) -> UpdateUserByIdCommand:
        return UpdateUserByIdCommand(user_service=user_service)
