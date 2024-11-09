import logging
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Final

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from library.adapters.database.di import DatabaseProvider
from library.application.exceptions import (
    EmptyPayloadException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
    LibraryException,
)
from library.domains.di import DomainProvider
from library.presentors.rest.config import RestConfig
from library.presentors.rest.routers.api.router import router as api_router
from library.presentors.rest.routers.api.v1.exception_handlers import (
    empty_payload_exception_handler,
    entity_already_exists_exception_handler,
    entity_not_found_exception_handler,
    http_exception_handler,
    library_exception_handler,
)

log = logging.getLogger(__name__)


ExceptionHandlersType = tuple[tuple[type[Exception], Callable], ...]

EXCEPTION_HANDLERS: Final[ExceptionHandlersType] = (
    (HTTPException, http_exception_handler),
    (LibraryException, library_exception_handler),
    (EntityNotFoundException, entity_not_found_exception_handler),
    (EmptyPayloadException, empty_payload_exception_handler),
    (EntityAlreadyExistsException, entity_already_exists_exception_handler),
)


@dataclass(frozen=True, slots=True, kw_only=True)
class RestService:
    config: RestConfig

    def create_application(self) -> FastAPI:
        app = FastAPI(
            debug=self.config.app.debug,
            title=self.config.app.title,
            description=self.config.app.description,
            version=self.config.app.version,
            openapi_url="/docs/openapi.json",
            docs_url="/docs/swagger",
            redoc_url="/docs/redoc",
            license_info={
                "name": "GNU 3.0",
                "url": "https://www.gnu.org/licenses/gpl-3.0.html",
            },
            contact={
                "name": "Sergey Natalenko",
                "url": "https://github.com/andy-takker",
                "email": "sergey.natalenko@mail.ru",
            },
            lifespan=lifespan,
        )

        self.set_middlewares(app=app)
        self.set_routes(app=app)
        self.set_exceptions(app=app)
        self.set_dependencies(app=app)

        log.info("REST service app configured")
        return app

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
        for exception, handler in EXCEPTION_HANDLERS:
            app.add_exception_handler(exception, handler)

    def set_dependencies(self, app: FastAPI) -> None:
        container = make_async_container(
            DatabaseProvider(
                dsn=self.config.database.dsn,
                debug=self.config.app.debug,
            ),
            DomainProvider(),
        )
        setup_dishka(container=container, app=app)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await app.state.dishka_container.close()
