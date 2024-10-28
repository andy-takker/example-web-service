import logging

from aiomisc import Service, entrypoint
from aiomisc_log import basic_config

from library.presentors.rest.config import RestConfig
from library.presentors.rest.service import RestService

log = logging.getLogger(__name__)


def main() -> None:
    config = RestConfig()
    basic_config(level=config.log.level)

    services: list[Service] = [
        RestService(
            host=config.host,
            port=config.port,
            config=config,
        )
    ]
    with entrypoint(
        *services,
        log_level=config.log.level,
        log_format=config.log.format,
        pool_size=config.app.pool_size,
        debug=config.app.debug,
    ) as loop:
        log.info("Starting services")
        loop.run_forever()


if __name__ == "__main__":
    main()
