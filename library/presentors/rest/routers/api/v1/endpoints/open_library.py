from typing import Annotated

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get
from litestar.params import Parameter

from library.domain.entities.open_library import OpenLibrarySearchParams
from library.domain.use_cases.queries.open_library.search import OpenLibrarySearchQuery
from library.presentors.rest.routers.api.v1.schemas.open_library import (
    OpenLibrarySearchSchema,
)


class OpenLibraryController(Controller):
    path = "/open-library"
    tags = ["Open Library"]

    @get("/search")
    @inject
    async def search(
        self,
        search_open_library: FromDishka[OpenLibrarySearchQuery],
        search_query: Annotated[
            str,
            Parameter(query="query", min_length=3, max_length=127),
        ],
        limit: Annotated[int, Parameter(ge=1, le=100)] = 10,
        offset: Annotated[int, Parameter(ge=0)] = 0,
    ) -> OpenLibrarySearchSchema:
        result = await search_open_library.execute(
            input_dto=OpenLibrarySearchParams(
                query=search_query,
                limit=limit,
                offset=offset,
            ),
        )
        return OpenLibrarySearchSchema.model_validate(result)
