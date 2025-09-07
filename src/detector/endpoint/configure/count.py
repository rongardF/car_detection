from fastapi import APIRouter
from uuid import UUID

from common import Injects

# local imports
from ...doc import Tags
from ...interface import AbstractAnalyzeConfigManager
from ...model.api import CountAnalysisConfigResponse, CountAnalysisConfigRequest
from ...exception import AnalyzerException, CountBadRequestException

router = APIRouter(tags=[Tags.CONFIGURE], prefix="/v1/configure/count")


@router.post(
    path="/",
    summary="Add configuration",
    description="Add configuration for object counting",
    status_code=200,
    responses={
        400: {"model": CountBadRequestException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def add_config(
    request: CountAnalysisConfigRequest,
    analysis_config_repository: AbstractAnalyzeConfigManager[CountAnalysisConfigRequest, CountAnalysisConfigResponse] = Injects("analyze_count_config_manager"),
) -> CountAnalysisConfigResponse:
    return await analysis_config_repository.add_config(request=request)


@router.get(
    path="/",
    summary="Get configuration",
    description="Get object counting configuration",
    status_code=200,
    responses={
        400: {"model": CountBadRequestException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def get_config(
    config_id: UUID,
    analysis_config_repository: AbstractAnalyzeConfigManager[CountAnalysisConfigRequest, CountAnalysisConfigResponse] = Injects("analyze_count_config_manager"),
) -> CountAnalysisConfigResponse:
    return await analysis_config_repository.get_config(config_id=config_id)


@router.patch(
    path="/",
    summary="Update configuration",
    description="Update object counting configuration",
    status_code=200,
    responses={
        400: {"model": CountBadRequestException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def update_config(
    config_id: UUID,
    request: CountAnalysisConfigRequest,
    analysis_config_repository: AbstractAnalyzeConfigManager[CountAnalysisConfigRequest, CountAnalysisConfigResponse] = Injects("analyze_count_config_manager"),
) -> CountAnalysisConfigResponse:
    return await analysis_config_repository.update_config(config_id=config_id, request=request)


@router.delete(
    path="/",
    summary="Delete configuration",
    description="Delete an object counting configuration",
    status_code=204,
    responses={
        400: {"model": CountBadRequestException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def delete_config(
    config_id: UUID,
    analysis_config_repository: AbstractAnalyzeConfigManager[CountAnalysisConfigRequest, CountAnalysisConfigResponse] = Injects("analyze_count_config_manager"),
) -> None:
    return await analysis_config_repository.delete_config(config_id=config_id)