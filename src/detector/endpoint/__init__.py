from fastapi import APIRouter

from . import health
from .analyze import count as analyze_count
from .configure import count as configure_count


main_router = APIRouter()

# add endpoint routers
main_router.include_router(analyze_count.router)
main_router.include_router(configure_count.router)
main_router.include_router(health.router)
