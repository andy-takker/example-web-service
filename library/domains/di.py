from dishka import Provider, Scope, provide

from library.domains.interfaces.storages.book import IBookStorage
from library.domains.services.book import BookService
from library.domains.use_cases.commands.create_book import CreateBookCommand
from library.domains.use_cases.commands.delete_book_by_id import DeleteBookByIdCommand
from library.domains.use_cases.commands.update_book_by_id import UpdateBookByIdCommand
from library.domains.use_cases.queries.fetch_book_by_id import FetchBookByIdQuery
from library.domains.use_cases.queries.fetch_book_list import FetchBookListQuery


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
