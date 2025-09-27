from fastapi import APIRouter, Depends

from ..authentication import authenticate

from . import health
from .analyze import count as analyze_count
from .configure import count as configure_count
from .account import user, authentication



main_router = APIRouter()

# add endpoint routers
main_router.include_router(analyze_count.router)
main_router.include_router(configure_count.router)
main_router.include_router(health.router)
main_router.include_router(user.router)
main_router.include_router(authentication.router)