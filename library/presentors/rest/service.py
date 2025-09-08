import logging
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from typing import Final

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from library.adapters.database.di import DatabaseProvider
from library.adapters.open_library.di import OpenLibraryProvider
from library.adapters.redis.di import RedisProvider
from library.application.exceptions import (
    EmptyPayloadException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
    LibraryException,
)
from library.application.logging import setup_logging
from library.config import Config
from library.domains.di import DomainProvider
from library.presentors.faststream.app_factory import get_faststream_app
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


def get_fastapi_app(config: Config) -> FastAPI:
    setup_logging(
        log_level=config.log.log_level,
        use_json=config.log.use_json,
    )
    faststream_app = get_faststream_app(config=config)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        await faststream_app.start()
        yield
        await faststream_app.stop()
        await app.state.dishka_container.close()

    app = FastAPI(
        debug=config.app.debug,
        title=config.app.title,
        description=config.app.description,
        version=config.app.version,
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

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    for exception, handler in EXCEPTION_HANDLERS:
        app.add_exception_handler(exception, handler)

    container = make_async_container(
        DatabaseProvider(
            dsn=config.database.dsn,
            debug=config.app.debug,
            max_overflow=config.database.max_overflow,
            pool_size=config.database.pool_size,
            pool_timeout=config.database.pool_timeout,
        ),
        DomainProvider(),
        OpenLibraryProvider(config=config.open_library),
        RedisProvider(config=config.redis),
    )
    setup_dishka(container=container, app=app)

    log.info("REST service app configured")
    return app
