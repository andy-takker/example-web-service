from dishka import Provider, Scope, provide

from library.domains.interfaces.storages.book import IBookStorage
from library.domains.services.book import BookService
from library.domains.use_cases.queries.fetch_book_by_id import FetchBookById
from library.domains.use_cases.queries.fetch_book_list import FetchBookList


class DomainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def book_service(self, book_storage: IBookStorage) -> BookService:
        return BookService(book_storage=book_storage)

    @provide(scope=Scope.REQUEST)
    def fetch_book_by_id(self, book_service: BookService) -> FetchBookById:
        return FetchBookById(book_service=book_service)

    @provide(scope=Scope.REQUEST)
    def fetch_book_list(self, book_service: BookService) -> FetchBookList:
        return FetchBookList(book_service=book_service)
