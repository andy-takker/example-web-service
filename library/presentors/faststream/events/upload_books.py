from collections.abc import Sequence

from pydantic import BaseModel


class UploadBooksEvent(BaseModel):
    queries: Sequence[str]
