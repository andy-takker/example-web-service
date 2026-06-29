from collections.abc import AsyncIterator

from aiocache import BaseCache
from aiohttp import ClientSession
from dishka import Provider, Scope, provide

from library.adapters.open_library.cached import CachedOpenLibraryClient
from library.adapters.open_library.client import OpenLibraryClient
from library.adapters.open_library.config import OpenLibraryConfig
from library.adapters.open_library.reduced import ReducedOpenLibraryClient
from library.domain.interfaces.clients.open_library import IOpenLibraryClient


class OpenLibraryProvider(Provider):
    scope = Scope.APP

    @provide()
    async def session(self) -> AsyncIterator[ClientSession]:
        async with ClientSession() as session:
            yield session

    @provide()
    def open_library_client(
        self,
        config: OpenLibraryConfig,
        session: ClientSession,
    ) -> OpenLibraryClient:
        return OpenLibraryClient(
            url=config.url,
            session=session,
            client_name="open_library",
        )

    @provide()
    def reduced_open_library_client(
        self, open_library_client: OpenLibraryClient
    ) -> ReducedOpenLibraryClient:
        return ReducedOpenLibraryClient(client=open_library_client)

    @provide()
    def cached_open_library_client(
        self, reduced_open_library_client: ReducedOpenLibraryClient, cache: BaseCache
    ) -> IOpenLibraryClient:
        return CachedOpenLibraryClient(client=reduced_open_library_client, cache=cache)
