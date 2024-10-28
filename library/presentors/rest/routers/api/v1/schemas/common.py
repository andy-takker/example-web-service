from pydantic import PositiveInt

from library.presentors.rest.schemas import BaseSchema


class StatusResponseSchema(BaseSchema):
    ok: bool
    status_code: PositiveInt
    message: str
