from typing import Annotated
from fastapi import APIRouter, UploadFile, Form, File
from uuid import UUID

from common import Injects

# local imports
from ...doc import Tags
from ...interface import AbstractVehicleCounter
from ...model.api.analysis.vehicle_count import VehicleCountResponse
from ...exception import AnalyzerException, CountBadRequestException
from ...database import CountAnalysisConfigRepository

# TODO: remove this after analysis config repository has been implemented
from ...model.detector import PixelCoordinate
from ...model.api.config import CountAnalysisConfigResponse, ImageResolution
from ...model.enum import ObjectEnum
##

router = APIRouter(tags=[Tags.DETECTION], prefix="/v1/count")


@router.post(
    path="/vehicle",
    summary="Count vehicles",
    description="Count number of vehicles on the uploaded image.",
    status_code=200,
    responses={
        400: {"model": CountBadRequestException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def count_vehicles(
    file: Annotated[UploadFile, File(title="Detection image")],
    analysis_config_id: UUID = Form(UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"), title="Analysis configuration ID"),
    vehicle_counter: AbstractVehicleCounter = Injects("vehicle_counter"),
    analysis_config_repository: CountAnalysisConfigRepository = Injects("analysis_config_repository"),
) -> VehicleCountResponse:
    analysis_config = await analysis_config_repository.get_one(entity_id=analysis_config_id)
    analysis_config_response = CountAnalysisConfigResponse.model_validate(analysis_config)
    return await vehicle_counter.count(file=file, count_analysis=analysis_config_response)
