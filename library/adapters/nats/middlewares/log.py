import logging
from typing import Any

from faststream import BaseMiddleware, StreamMessage
from faststream.types import AsyncFuncAny

log = logging.getLogger("faststream")


class LogMessageMetaMiddleware(BaseMiddleware):
    async def on_consume(self, msg: StreamMessage[Any]) -> StreamMessage[Any]:
        # Log message with redelivered info for debug race condition

        metadata, consumer, num_delivered = _get_metadata(msg)
        _log_level = (
            logging.WARNING if num_delivered and num_delivered > 1 else logging.INFO
        )

        log.log(
            _log_level,
            "[JetStream] Received message: ID=%s, Redelivered=%s, Consumer=%s.",
            msg.message_id,
            num_delivered,
            consumer,
        )
        return await super().on_consume(msg)

    async def after_consume_with_message(
        self, message: StreamMessage[Any], err: Exception | None
    ) -> None:
        if err is not None:
            metadata, consumer, num_delivered = _get_metadata(message)

            log.error(
                "[JetStream] Message(ID=%s, Redelivered=%s, Consumer=%s) "
                "processing failed.",
                message.message_id,
                num_delivered,
                consumer,
                exc_info=err,
            )

        await self.after_consume(err)

    async def consume_scope(
        self,
        call_next: AsyncFuncAny,
        msg: StreamMessage[Any],
    ) -> Any:
        err: Exception | None = None
        try:
            result = await call_next(await self.on_consume(msg))

        except Exception as e:  # noqa: BLE001
            err = e

        else:
            return result

        finally:
            await self.after_consume_with_message(msg, err)


def _get_metadata(
    message: StreamMessage[Any],
) -> tuple[Any | None, Any | None, Any | None]:
    metadata = getattr(message.raw_message, "metadata", None)
    consumer = metadata.consumer if metadata and hasattr(metadata, "consumer") else None
    num_delivered = (
        metadata.num_delivered
        if metadata and hasattr(metadata, "num_delivered")
        else None
    )

    return metadata, consumer, num_delivered
