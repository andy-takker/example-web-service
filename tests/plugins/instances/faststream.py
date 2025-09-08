from collections.abc import AsyncIterator

import pytest
from faststream import FastStream
from faststream.nats import NatsBroker, StreamConfig, TestNatsBroker

from library.adapters.nats.broker import create_broker
from library.adapters.nats.config import NatsConfig
from library.adapters.nats.stream import STREAM
from library.config import Config
from library.presentors.faststream.app_factory import get_faststream_app
from library.presentors.faststream.subjects import BooksSubjects


@pytest.fixture
def broker(nats_config: NatsConfig) -> NatsBroker:
    return create_broker(nats_config)


@pytest.fixture
async def setup_stream(broker: NatsBroker) -> None:
    async with broker as _broker:
        await prepare_stream(_broker)


@pytest.fixture
async def faststream_app(config: Config, setup_stream, clear_redis_cache) -> FastStream:
    app = get_faststream_app(config=config)
    yield app
    await app.stop()


@pytest.fixture()
async def faststream_client(faststream_app: FastStream) -> AsyncIterator[NatsBroker]:
    async with TestNatsBroker(faststream_app.broker, with_real=True) as broker:
        yield broker


async def prepare_stream(broker: NatsBroker) -> None:
    for stream in await broker.stream.streams_info():
        await broker.stream.delete_stream(name=stream.config.name)
    await broker.stream.add_stream(
        config=StreamConfig(
            name=STREAM.name,
            subjects=[BooksSubjects.UPLOAD_OPEN_LIBRARY],
        )
    )
