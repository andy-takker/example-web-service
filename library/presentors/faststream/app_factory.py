from dishka import make_async_container
from dishka_faststream import setup_dishka
from faststream import FastStream

from library.adapters.database.config import DatabaseConfig
from library.adapters.database.di import DatabaseProvider
from library.adapters.nats.broker import create_broker
from library.adapters.open_library.config import OpenLibraryConfig
from library.adapters.open_library.di import OpenLibraryProvider
from library.adapters.redis.config import RedisConfig
from library.adapters.redis.di import RedisProvider
from library.application.config import AppConfig
from library.config import Config
from library.domain.di import DomainProvider
from library.presentors.faststream.handlers.router import router


def get_faststream_app(config: Config) -> FastStream:
    broker = create_broker(config.nats)
    faststream_app = FastStream(broker)
    container = make_async_container(
        DatabaseProvider(),
        DomainProvider(),
        OpenLibraryProvider(),
        RedisProvider(),
        context={
            RedisConfig: config.redis,
            OpenLibraryConfig: config.open_library,
            DatabaseConfig: config.database,
            AppConfig: config.app,
        },
    )
    setup_dishka(container, faststream_app, auto_inject=True)
    broker.include_router(router)
    return faststream_app
