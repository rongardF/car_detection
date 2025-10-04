from typing import Annotated
from fastapi import APIRouter, UploadFile, Form, File, Depends
from uuid import UUID

from common import Injects

# local imports
from ...doc import Tags
from ...authentication import authenticate
from ...interface import AbstractImageAnalyzer, AbstractAnalyzeImageConfigManager
from ...model.api import ObjectAnalysisConfigResponse, ObjectAnalysisConfigRequest, ObjectCountResponse, ObjectLocationResponse
from ...exception import AnalyzerException, AnalyzeBadRequestException, AnalyzeNotFoundException, ConfigureNotFoundException

router = APIRouter(tags=[Tags.ANALYZE, Tags.IMAGE], prefix="/v1/analyze/image")

# region: image
@router.post(
    path="/object/count",
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
    account_id: UUID = Depends(authenticate),
    analysisConfigId: UUID = Form(UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"), title="Analysis configuration ID"),
    image_analyzer: AbstractImageAnalyzer = Injects("image_analyzer"),
    analyze_object_config_manager: AbstractAnalyzeImageConfigManager[ObjectAnalysisConfigRequest, ObjectAnalysisConfigResponse] = Injects("analyze_object_config_manager"),
) -> list[ObjectCountResponse]:
    try:
        analysis_config = await analyze_object_config_manager.get_config(account_id=account_id, config_id=analysisConfigId)
    except ConfigureNotFoundException:
        raise AnalyzeNotFoundException(detail="configuration_entity_not_found")
    return await image_analyzer.count_objects(file=file, count_analysis=analysis_config)


@router.post(
    path="/object/locate",
    summary="Locate objects",
    description="Locate objects in the provided image",
    status_code=200,
    responses={
        400: {"model": AnalyzeBadRequestException.model},
        404: {"model": AnalyzeNotFoundException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def locate_objects(
    file: Annotated[UploadFile, File(title="Detection image")],
    account_id: UUID = Depends(authenticate),
    analysisConfigId: UUID = Form(UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"), title="Analysis configuration ID"),
    image_analyzer: AbstractImageAnalyzer = Injects("image_analyzer"),
    analyze_object_config_manager: AbstractAnalyzeImageConfigManager[ObjectAnalysisConfigRequest, ObjectAnalysisConfigResponse] = Injects("analyze_object_config_manager"),
) -> list[ObjectLocationResponse]:
    try:
        analysis_config = await analyze_object_config_manager.get_config(account_id=account_id, config_id=analysisConfigId)
    except ConfigureNotFoundException:
        raise AnalyzeNotFoundException(detail="configuration_entity_not_found")
    return await image_analyzer.locate_objects(file=file, count_analysis=analysis_config)
# endregion: image