from fastapi import APIRouter

from . import health
from .analyze import count

main_router = APIRouter()

# add endpoint routers
main_router.include_router(count.router)
main_router.include_router(health.router)
