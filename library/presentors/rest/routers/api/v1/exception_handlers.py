from http import HTTPStatus

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from library.application.exceptions import (
    EmptyPayloadException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
    LibraryException,
)
from library.presentors.rest.routers.api.v1.schemas.common import StatusResponseSchema


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return exception_json_response(
        status_code=exc.status_code,
        message=exc.detail,
    )


async def entity_not_found_exception_handler(
    request: Request,
    exc: EntityNotFoundException,
) -> JSONResponse:
    return exception_json_response(
        status_code=HTTPStatus.NOT_FOUND,
        message=exc.message,
    )


async def empty_payload_exception_handler(
    request: Request,
    exc: EmptyPayloadException,
) -> JSONResponse:
    return exception_json_response(
        status_code=HTTPStatus.BAD_REQUEST,
        message=exc.message,
    )


async def library_exception_handler(
    request: Request,
    exc: LibraryException,
) -> JSONResponse:
    return exception_json_response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        message=exc.message,
    )


async def entity_already_exists_exception_handler(
    request: Request,
    exc: EntityAlreadyExistsException,
) -> JSONResponse:
    return exception_json_response(
        status_code=HTTPStatus.CONFLICT,
        message=exc.message,
    )


def exception_json_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=StatusResponseSchema(
            ok=False,
            status_code=status_code,
            message=message,
        ).model_dump(mode="json"),
    )
