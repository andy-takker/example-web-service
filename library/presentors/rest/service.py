import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.litestar import setup_dishka
from litestar import Litestar
from litestar.config.compression import CompressionConfig
from litestar.config.cors import CORSConfig
from litestar.exceptions import HTTPException, ValidationException
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import RedocRenderPlugin, SwaggerRenderPlugin
from litestar.plugins.prometheus import PrometheusConfig, PrometheusController

from library.adapters.database.config import DatabaseConfig
from library.adapters.database.di import DatabaseProvider
from library.adapters.open_library.config import OpenLibraryConfig
from library.adapters.open_library.di import OpenLibraryProvider
from library.adapters.redis.config import RedisConfig
from library.adapters.redis.di import RedisProvider
from library.application.config import AppConfig
from library.application.exceptions import (
    EmptyPayloadException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
    LibraryException,
)
from library.application.logging import setup_logging
from library.application.sentry import setup_sentry
from library.config import Config
from library.domain.di import DomainProvider
from library.presentors.faststream.app_factory import get_faststream_app
from library.presentors.rest.routers.api.router import router as api_router
from library.presentors.rest.routers.api.v1.exception_handlers import (
    empty_payload_exception_handler,
    entity_already_exists_exception_handler,
    entity_not_found_exception_handler,
    http_exception_handler,
    library_exception_handler,
    validation_exception_handler,
)

log = logging.getLogger(__name__)


def get_litestar_app(config: Config) -> Litestar:
    setup_logging(
        log_level=config.log.log_level,
        use_json=config.log.use_json,
    )

    if config.sentry.use_sentry:
        setup_sentry(dsn=config.sentry.dsn, env=config.sentry.env)

    faststream_app = get_faststream_app(config=config)

    @asynccontextmanager
    async def lifespan(app: Litestar) -> AsyncIterator[None]:
        await faststream_app.start()
        yield
        await faststream_app.stop()
        await app.state.dishka_container.close()

    prometheus_config = PrometheusConfig(group_path=True, exclude=["/docs"])
    rate_limit_config = RateLimitConfig(
        rate_limit=("minute", 100),
        exclude=[
            "/docs/redoc",
            "/docs/swagger",
            "/metrics",
        ],
    )

    app = Litestar(
        lifespan=[lifespan],
        route_handlers=[
            PrometheusController,
            api_router,
        ],
        logging_config=None,
        middleware=[prometheus_config.middleware, rate_limit_config.middleware],
        exception_handlers={
            ValidationException: validation_exception_handler,
            HTTPException: http_exception_handler,
            LibraryException: library_exception_handler,
            EntityNotFoundException: entity_not_found_exception_handler,
            EmptyPayloadException: empty_payload_exception_handler,
            EntityAlreadyExistsException: entity_already_exists_exception_handler,
        },
        openapi_config=OpenAPIConfig(
            title=config.app.title,
            description=config.app.description,
            version=config.app.version,
            path="/docs",
            render_plugins=[
                RedocRenderPlugin(path="/redoc"),
                SwaggerRenderPlugin(path="/swagger"),
            ],
        ),
        cors_config=CORSConfig(
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        compression_config=CompressionConfig(backend="gzip", gzip_compress_level=9),
        debug=config.app.debug,
    )

    container = make_async_container(
        DatabaseProvider(),
        DomainProvider(),
        OpenLibraryProvider(),
        RedisProvider(),
        context={
            AppConfig: config.app,
            DatabaseConfig: config.database,
            OpenLibraryConfig: config.open_library,
            RedisConfig: config.redis,
        },
    )
    setup_dishka(container=container, app=app)

    log.info("REST service app configured")
    return app
