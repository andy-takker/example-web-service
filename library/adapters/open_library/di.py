from collections.abc import AsyncIterator

from aiocache import BaseCache
from aiohttp import ClientSession
from dishka import BaseScope, Component, Provider, Scope, provide

from library.adapters.open_library.cached import CachedOpenLibraryClient
from library.adapters.open_library.client import OpenLibraryClient
from library.adapters.open_library.config import OpenLibraryConfig
from library.adapters.open_library.reduced import ReducedOpenLibraryClient
from library.domains.interfaces.clients.open_library import IOpenLibraryClient


class OpenLibraryProvider(Provider):
    def __init__(
        self,
        config: OpenLibraryConfig,
        scope: BaseScope | None = None,
        component: Component | None = None,
    ):
        super().__init__(scope, component)
        self._config = config

    @provide(scope=Scope.APP)
    async def session(self) -> AsyncIterator[ClientSession]:
        async with ClientSession() as session:
            yield session

    @provide(scope=Scope.APP)
    def open_library_client(self, session: ClientSession) -> OpenLibraryClient:
        return OpenLibraryClient(
            url=self._config.url,
            session=session,
            client_name="open_library",
        )

    @provide(scope=Scope.APP)
    def reduced_open_library_client(
        self, open_library_client: OpenLibraryClient
    ) -> ReducedOpenLibraryClient:
        return ReducedOpenLibraryClient(client=open_library_client)

    @provide(scope=Scope.APP)
    def cached_open_library_client(
        self, reduced_open_library_client: ReducedOpenLibraryClient, cache: BaseCache
    ) -> IOpenLibraryClient:
        return CachedOpenLibraryClient(client=reduced_open_library_client, cache=cache)
