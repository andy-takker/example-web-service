import uvicorn

from library.config import Config
from library.presentors.rest.service import get_litestar_app


def main() -> None:
    config = Config()
    litestar_app = get_litestar_app(config=config)

    uvicorn.run(
        litestar_app,
        host=config.http.host,
        port=config.http.port,
        forwarded_allow_ips="*",
        log_config=None,
    )


if __name__ == "__main__":
    main()
