import logging

from faststream.nats import NatsBroker
from faststream.nats.prometheus import NatsPrometheusMiddleware
from prometheus_client import CollectorRegistry

from library.adapters.nats.config import NatsConfig
from library.adapters.nats.middlewares.log import LogMessageMetaMiddleware

log = logging.getLogger("faststream")


def create_broker(
    config: NatsConfig, prometheus_registry: CollectorRegistry | None = None
) -> NatsBroker:
    middlewares = [LogMessageMetaMiddleware]
    if prometheus_registry:
        middlewares.append(
            NatsPrometheusMiddleware(
                registry=prometheus_registry,
                app_name=config.name,
            ),  # type: ignore
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
