from typing import Any


class LibraryException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class EntityNotFoundException(LibraryException):
    def __init__(self, entity: type, entity_id: Any) -> None:
        super().__init__(f"{entity.__name__} with id {entity_id} not found")


class EmptyPayloadException(LibraryException): ...


class EntityAlreadyExistsException(LibraryException): ...
