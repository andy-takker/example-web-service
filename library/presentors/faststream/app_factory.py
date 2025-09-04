from dishka import make_async_container
from dishka.integrations.faststream import setup_dishka
from faststream import FastStream

from library.adapters.database.di import DatabaseProvider
from library.adapters.nats.broker import create_broker
from library.adapters.open_library.di import OpenLibraryProvider
from library.adapters.redis.di import RedisProvider
from library.config import Config
from library.domains.di import DomainProvider
from library.presentors.faststream.handlers.router import router


def get_faststream_app(config: Config) -> FastStream:
    broker = create_broker(config.nats)
    faststream_app = FastStream(broker=broker)
    container = make_async_container(
        DatabaseProvider(
            dsn=config.database.dsn,
            pool_size=config.database.pool_size,
            pool_timeout=config.database.pool_timeout,
            max_overflow=config.database.max_overflow,
            debug=config.app.debug,
        ),
        DomainProvider(),
        OpenLibraryProvider(config.open_library),
        RedisProvider(config=config.redis),
    )
    setup_dishka(container, faststream_app, auto_inject=True)
    broker.include_router(router)
    return faststream_app
