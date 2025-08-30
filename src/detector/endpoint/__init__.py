from fastapi import APIRouter

from . import detect, health

main_router = APIRouter()

# add endpoint routers
main_router.include_router(detect.router)
main_router.include_router(health.router)
