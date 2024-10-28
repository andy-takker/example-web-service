from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"], route_class=DishkaRoute)
