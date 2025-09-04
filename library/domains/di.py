from dishka import Provider, Scope, provide

from library.domains.interfaces.clients.open_library import IOpenLibraryClient
from library.domains.interfaces.storages.book import IBookStorage
from library.domains.interfaces.storages.user import IUserStorage
from library.domains.services.book import BookService
from library.domains.services.user import UserService
from library.domains.uow import AbstractUow
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
from library.domains.use_cases.queries.open_library.search import OpenLibrarySearchQuery
from library.domains.use_cases.queries.user.fetch_user_by_id import FetchUserByIdQuery
from library.domains.use_cases.queries.user.fetch_user_list import FetchUserListQuery


class DomainProvider(Provider):
    scope = Scope.REQUEST

    @provide()
    def book_service(self, book_storage: IBookStorage) -> BookService:
        return BookService(book_storage=book_storage)

    @provide()
    def fetch_book_by_id(
        self, uow: AbstractUow, book_service: BookService
    ) -> FetchBookByIdQuery:
        return FetchBookByIdQuery(uow=uow, book_service=book_service)

    @provide()
    def fetch_book_list(
        self, uow: AbstractUow, book_service: BookService
    ) -> FetchBookListQuery:
        return FetchBookListQuery(uow=uow, book_service=book_service)

    @provide()
    def create_book_command(
        self, uow: AbstractUow, book_service: BookService
    ) -> CreateBookCommand:
        return CreateBookCommand(uow=uow, book_service=book_service)

    @provide()
    def delete_book_by_id_command(
        self, uow: AbstractUow, book_service: BookService
    ) -> DeleteBookByIdCommand:
        return DeleteBookByIdCommand(uow=uow, book_service=book_service)

    @provide()
    def update_book_by_id_command(
        self, uow: AbstractUow, book_service: BookService
    ) -> UpdateBookByIdCommand:
        return UpdateBookByIdCommand(uow=uow, book_service=book_service)

    @provide()
    def user_service(self, user_storage: IUserStorage) -> UserService:
        return UserService(user_storage=user_storage)

    @provide()
    def fetch_user_by_id(
        self, uow: AbstractUow, user_service: UserService
    ) -> FetchUserByIdQuery:
        return FetchUserByIdQuery(uow=uow, user_service=user_service)

    @provide()
    def fetch_user_list(
        self, uow: AbstractUow, user_service: UserService
    ) -> FetchUserListQuery:
        return FetchUserListQuery(uow=uow, user_service=user_service)

    @provide()
    def create_user_command(
        self, uow: AbstractUow, user_service: UserService
    ) -> CreateUserCommand:
        return CreateUserCommand(uow=uow, user_service=user_service)

    @provide()
    def delete_user_by_id_command(
        self, uow: AbstractUow, user_service: UserService
    ) -> DeleteUserByIdCommand:
        return DeleteUserByIdCommand(uow=uow, user_service=user_service)

    @provide()
    def update_user_by_id_command(
        self, uow: AbstractUow, user_service: UserService
    ) -> UpdateUserByIdCommand:
        return UpdateUserByIdCommand(uow=uow, user_service=user_service)

    @provide()
    def open_library_search_query(
        self, client: IOpenLibraryClient
    ) -> OpenLibrarySearchQuery:
        return OpenLibrarySearchQuery(client=client)
