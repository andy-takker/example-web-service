from fastapi import APIRouter

from library.presentors.rest.routers.api.v1.endpoints.books import (
    router as books_router,
)
from library.presentors.rest.routers.api.v1.endpoints.users import (
    router as users_router,
)

router = APIRouter(prefix="/v1")
router.include_router(users_router)
router.include_router(books_router)
