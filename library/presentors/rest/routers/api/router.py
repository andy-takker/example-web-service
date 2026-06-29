from litestar import Router

from library.presentors.rest.routers.api.v1.router import router as v1_router

router = Router(path="/api", route_handlers=[v1_router])
