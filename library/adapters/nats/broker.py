import logging
from typing import Any, Self

from faststream import BaseMiddleware
from faststream.broker.message import StreamMessage
from faststream.broker.types import BrokerMiddleware
from faststream.nats import NatsBroker
from faststream.nats.prometheus import NatsPrometheusMiddleware
from prometheus_client import CollectorRegistry

from library.adapters.nats.config import NatsConfig

log = logging.getLogger("faststream")


class LogMessageMetaMiddleware(BaseMiddleware):
    def __call__(self, _msg: Any) -> Self:
        return self

    async def on_consume(self, message: StreamMessage[Any]) -> StreamMessage[Any]:
        # Log message with redelivered info for debug race condition

        metadata = getattr(message.raw_message, "metadata", None)
        consumer = (
            metadata.consumer if metadata and hasattr(metadata, "consumer") else None
        )
        num_delivered = (
            metadata.num_delivered
            if metadata and hasattr(metadata, "num_delivered")
            else None
        )
        _log_level = (
            logging.WARNING if num_delivered and num_delivered > 1 else logging.INFO
        )

        log.log(
            _log_level,
            "[JetStream] Received message: ID=%s, Redelivered=%s, Consumer=%s",
            message.message_id,
            num_delivered,
            consumer,
        )
        return await super().on_consume(message)


def create_broker(
    config: NatsConfig, prometheus_registry: CollectorRegistry | None = None
) -> NatsBroker:
    log_message_middleware = LogMessageMetaMiddleware()
    middlewares: list[BrokerMiddleware] = [
        log_message_middleware,
    ]
    if prometheus_registry:
        middlewares.append(
            NatsPrometheusMiddleware(
                registry=prometheus_registry,
                app_name=config.name,
            ),
        )
    return NatsBroker(
        servers=[config.dsn],
        logger=logging.getLogger("broker"),
        name=config.name,
        middlewares=middlewares,
        connect_timeout=config.connect_timeout,
        reconnect_time_wait=config.reconnect_time_wait,
        max_reconnect_attempts=config.max_reconnect_attempts,
        allow_reconnect=config.allow_reconnect,
    )
