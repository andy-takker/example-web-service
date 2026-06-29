from http import HTTPStatus

from litestar import MediaType, Request, Response
from litestar.exceptions import HTTPException, ValidationException

from library.application.exceptions import (
    EmptyPayloadException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
    LibraryException,
)
from library.presentors.rest.routers.api.v1.schemas.common import StatusResponseSchema


def validation_exception_handler(
    request: Request,
    exc: ValidationException,
) -> Response[StatusResponseSchema]:
    return exception_json_response(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        message=exc.detail,
    )


def http_exception_handler(
    request: Request, exc: HTTPException
) -> Response[StatusResponseSchema]:
    return exception_json_response(
        status_code=exc.status_code,
        message=exc.detail,
    )


def entity_not_found_exception_handler(
    request: Request,
    exc: EntityNotFoundException,
) -> Response[StatusResponseSchema]:
    return exception_json_response(
        status_code=HTTPStatus.NOT_FOUND,
        message=exc.message,
    )


def empty_payload_exception_handler(
    request: Request,
    exc: EmptyPayloadException,
) -> Response[StatusResponseSchema]:
    return exception_json_response(
        status_code=HTTPStatus.BAD_REQUEST,
        message=exc.message,
    )


def library_exception_handler(
    request: Request,
    exc: LibraryException,
) -> Response[StatusResponseSchema]:
    return exception_json_response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        message=exc.message,
    )


def entity_already_exists_exception_handler(
    request: Request,
    exc: EntityAlreadyExistsException,
) -> Response[StatusResponseSchema]:
    return exception_json_response(
        status_code=HTTPStatus.CONFLICT,
        message=exc.message,
    )


def exception_json_response(
    status_code: int, message: str
) -> Response[StatusResponseSchema]:
    return Response(
        status_code=status_code,
        content=StatusResponseSchema(
            ok=False,
            status_code=status_code,
            message=message,
        ),
        media_type=MediaType.JSON,
    )
