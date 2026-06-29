from litestar import Router

from library.presentors.rest.routers.api.v1.endpoints.books import (
    BooksController,
)
from library.presentors.rest.routers.api.v1.endpoints.open_library import (
    OpenLibraryController,
)
from library.presentors.rest.routers.api.v1.endpoints.users import (
    UsersController,
)

router = Router(
    path="/v1",
    route_handlers=[
        BooksController,
        OpenLibraryController,
        UsersController,
    ],
)
