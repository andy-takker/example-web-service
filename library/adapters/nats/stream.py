from typing import Final

from faststream.nats import JStream

MAX_AGE_SECONDS = 60 * 60

STREAM: Final[JStream] = JStream(
    name="base_stream",
    max_age=MAX_AGE_SECONDS,
)
