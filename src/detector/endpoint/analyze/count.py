from typing import Annotated
from fastapi import APIRouter, UploadFile, Form, File
from uuid import UUID

from common import Injects

# local imports
from ...doc import Tags
from ...interface import AbstractObjectCounter, AbstractAnalyzeConfigManager
from ...model.api import CountAnalysisConfigResponse, CountAnalysisConfigRequest, VehicleCountResponse
from ...exception import AnalyzerException, CountBadRequestException

router = APIRouter(tags=[Tags.ANALYZE], prefix="/v1/analyze/count")


@router.post(
    path="/",
    summary="Count objects",
    description="Count number of objects in the provided image",
    status_code=200,
    responses={
        400: {"model": CountBadRequestException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def count_objects(
    file: Annotated[UploadFile, File(title="Detection image")],
    analysis_config_id: UUID = Form(UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"), title="Analysis configuration ID"),
    vehicle_counter: AbstractObjectCounter = Injects("vehicle_counter"),
    analyze_count_config_manager: AbstractAnalyzeConfigManager[CountAnalysisConfigRequest, CountAnalysisConfigResponse] = Injects("analyze_count_config_manager"),
) -> VehicleCountResponse:
    analysis_config = await analyze_count_config_manager.get_config(config_id=analysis_config_id)
    return await vehicle_counter.count(file=file, count_analysis=analysis_config)
