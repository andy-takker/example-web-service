from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query

from library.domains.entities.open_library import OpenLibrarySearchParams
from library.domains.use_cases.queries.open_library.search import OpenLibrarySearchQuery
from library.presentors.rest.routers.api.v1.schemas.open_library import (
    OpenLibrarySearchSchema,
)

router = APIRouter(prefix="/open-library", route_class=DishkaRoute)


@router.get("/search")
async def search(
    search_open_library: FromDishka[OpenLibrarySearchQuery],
    query: str = Query(min_length=3, max_length=127),
    limit: int = Query(ge=1, le=100, default=10),
    offset: int = Query(ge=0, default=0),
) -> OpenLibrarySearchSchema:
    result = await search_open_library.execute(
        input_dto=OpenLibrarySearchParams(query=query, limit=limit, offset=offset),
    )
    return OpenLibrarySearchSchema.model_validate(result)
