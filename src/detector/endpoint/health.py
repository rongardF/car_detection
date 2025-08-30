from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/health", include_in_schema=False, response_class=PlainTextResponse)
async def get_health() -> PlainTextResponse:
    return PlainTextResponse("OK")