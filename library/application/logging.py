import logging
import sys
from dataclasses import dataclass, field
from enum import StrEnum, unique
from os import environ
from types import TracebackType

import structlog


@unique
class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def setup_logging(log_level: LogLevel = LogLevel.INFO, use_json: bool = False) -> None:
    shared_processors: list[structlog.typing.Processor] = [
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.contextvars.merge_contextvars,
    ]
    structlog.configure(
        processors=shared_processors
        + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    log_renderer: structlog.types.Processor
    if use_json:
        log_renderer = structlog.processors.JSONRenderer()
    else:
        log_renderer = structlog.dev.ConsoleRenderer()
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            log_renderer,
        ],
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level.upper())

    for _log in [
        "_granian",
        "granian.access",
        "granian.error",
        "faststream",
        "pytest",
    ]:
        logging.getLogger(_log).handlers.clear()
        logging.getLogger(_log).propagate = True

    def handle_exception(
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType | None,
    ) -> None:
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.error(
            "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
        )

    sys.excepthook = handle_exception


@dataclass(frozen=True, kw_only=True, slots=True)
class LoggingConfig:
    log_level: LogLevel = field(
        default_factory=lambda: LogLevel(environ.get("APP_LOG_LEVEL", "DEBUG").upper())
    )
    use_json: bool = field(
        default_factory=lambda: environ.get("APP_LOG_JSON", "false").lower() == "true"
    )
