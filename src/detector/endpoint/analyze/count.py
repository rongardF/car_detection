from typing import Annotated
from fastapi import APIRouter, UploadFile, Form, File, Depends
from uuid import UUID

from common import Injects

# local imports
from ...doc import Tags
from ...authentication import authenticate
from ...interface import AbstractObjectCounter, AbstractAnalyzeConfigManager
from ...model.api import CountAnalysisConfigResponse, CountAnalysisConfigRequest, ObjectCountResponse
from ...exception import AnalyzerException, AnalyzeBadRequestException, AnalyzeNotFoundException, ConfigureNotFoundException

router = APIRouter(tags=[Tags.ANALYZE], prefix="/v1/analyze/count")


@router.post(
    path="/",
    summary="Count objects",
    description="Count number of objects in the provided image",
    status_code=200,
    responses={
        400: {"model": AnalyzeBadRequestException.model},
        404: {"model": AnalyzeNotFoundException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def count_objects(
    file: Annotated[UploadFile, File(title="Detection image")],
    user_id: UUID = Depends(authenticate),
    analysis_config_id: UUID = Form(UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"), title="Analysis configuration ID"),
    object_counter: AbstractObjectCounter = Injects("object_counter"),
    analyze_count_config_manager: AbstractAnalyzeConfigManager[CountAnalysisConfigRequest, CountAnalysisConfigResponse] = Injects("analyze_count_config_manager"),
) -> ObjectCountResponse:
    try:
        analysis_config = await analyze_count_config_manager.get_config(user_id=user_id, config_id=analysis_config_id)
    except ConfigureNotFoundException:
        raise AnalyzeNotFoundException(detail="configuration_entity_not_found")
    return await object_counter.count(file=file, count_analysis=analysis_config)
