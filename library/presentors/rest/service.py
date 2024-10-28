import logging
from collections.abc import Callable

from aiomisc.service.uvicorn import UvicornApplication, UvicornService
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from library.adapters.database.di import DatabaseProvider
from library.application.exceptions import EntityNotFoundException, LibraryException
from library.domains.di import DomainProvider
from library.presentors.rest.config import RestConfig
from library.presentors.rest.routers.api.router import router as api_router
from library.presentors.rest.routers.api.v1.handlers import (
    entity_not_found_exception_handler,
    http_exception_handler,
    library_exception_handler,
)

log = logging.getLogger(__name__)


ExceptionHandlersType = tuple[tuple[type[Exception], Callable], ...]


class RestService(UvicornService):
    config: RestConfig

    __required__ = ("config",)

    container: AsyncContainer

    EXCEPTION_HANDLERS: ExceptionHandlersType = (
        (HTTPException, http_exception_handler),
        (LibraryException, library_exception_handler),
        (EntityNotFoundException, entity_not_found_exception_handler),
    )

    async def create_application(self) -> UvicornApplication:
        app = FastAPI(
            debug=self.config.app.debug,
            title=self.config.app.title,
            description=self.config.app.description,
            version=self.config.app.version,
            openapi_url="/docs/openapi.json",
            docs_url="/docs/swagger",
            redoc_url="/docs/redoc",
        )

        self.set_middlewares(app=app)
        self.set_routes(app=app)
        self.set_exceptions(app=app)
        self.set_dependencies(app=app)

        log.info("REST service app configured")
        return app

    async def stop(self, exception: Exception | None = None) -> None:
        await self.container.close(exception=exception)

    def set_middlewares(self, app: FastAPI) -> None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def set_routes(self, app: FastAPI) -> None:
        app.include_router(api_router)

    def set_exceptions(self, app: FastAPI) -> None:
        for exception, handler in self.EXCEPTION_HANDLERS:
            app.add_exception_handler(exception, handler)

    def set_dependencies(self, app: FastAPI) -> None:
        self.container = make_async_container(
            DatabaseProvider(
                dsn=self.config.database.dsn,
                debug=self.config.app.debug,
            ),
            DomainProvider(),
        )
        setup_dishka(container=self.container, app=app)
