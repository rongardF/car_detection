from fastapi import APIRouter

from . import health
from .analyze import image as analyze_image
from .configure import image as configure_image_analysis
from .account import user, authentication


main_router = APIRouter()

# add endpoint routers
main_router.include_router(analyze_image.router)
main_router.include_router(configure_image_analysis.router)
main_router.include_router(health.router)
main_router.include_router(user.router)
main_router.include_router(authentication.router)