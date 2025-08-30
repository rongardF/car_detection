from fastapi import APIRouter

from common import Injects

# local imports
from ..doc import Tags
from ..interface import AbstractProcessor

router = APIRouter(tags=[], prefix="/v1/detect")


@router.get(
    path="/detect",
    summary="Detection",
    description="Detect number of cars on the image.",
    status_code=200,
    # responses={
    #     403: {"model": AccessDenied.model},
    #     500: {"model": GiamException.model},
    # },
)
async def access_evaluate(
    # request: EvaluateRequest,
    processor: AbstractProcessor = Injects("processor"),
) -> None:
    try:
        return None
    except Exception as exc:
        raise exc