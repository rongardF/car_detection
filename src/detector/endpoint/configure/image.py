from fastapi import APIRouter, Security
from uuid import UUID

from common import Injects

# local imports
from ...authentication import authenticate
from ...doc import Tags
from ...model.enum import AuthorizationScopeEnum
from ...interface import AbstractAnalyzeImageConfigManager
from ...model.api import ObjectAnalysisConfigRequest, ObjectAnalysisConfigResponse
from ...exception import AnalyzerException, ConfigureBadRequestException, ConfigureNotFoundException, AccountUnAuthorizedException

router = APIRouter(tags=[Tags.CONFIGURE, Tags.IMAGE], prefix="/v1/configure/image")

# region: object
@router.post(
    path="/object",
    summary="Add configuration",
    description="Add configuration for analyzing image for objects",
    status_code=200,
    responses={
        400: {"model": ConfigureBadRequestException.model},
        401: {"model": AccountUnAuthorizedException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def add_config(
    request: ObjectAnalysisConfigRequest,
    account_id: UUID = Security(authenticate, scopes=[AuthorizationScopeEnum.CONFIGURE.value]),
    analyze_object_config_manager: AbstractAnalyzeImageConfigManager[ObjectAnalysisConfigRequest, ObjectAnalysisConfigResponse] = Injects("analyze_object_config_manager"),
) -> ObjectAnalysisConfigResponse:
    return await analyze_object_config_manager.add_config(account_id=account_id, request=request)


@router.get(
    path="/object/{configId}",
    summary="Get configuration",
    description="Get configuration for analyzing image for objects",
    status_code=200,
    responses={
        404: {"model": ConfigureNotFoundException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def get_config(
    configId: UUID,
    account_id: UUID = Security(authenticate, scopes=[AuthorizationScopeEnum.CONFIGURE.value]),
    analyze_object_config_manager: AbstractAnalyzeImageConfigManager[ObjectAnalysisConfigRequest, ObjectAnalysisConfigResponse] = Injects("analyze_object_config_manager"),
) -> ObjectAnalysisConfigResponse:
    return await analyze_object_config_manager.get_config(account_id=account_id, config_id=configId)

@router.get(
    path="/object",
    summary="Get all configurations",
    description="Get all configurations for objects analysis on image(s)",
    status_code=200,
    responses={
        500: {"model": AnalyzerException.model},
    },
)
async def get_all_configs(
    account_id: UUID = Security(authenticate, scopes=[AuthorizationScopeEnum.CONFIGURE.value]),
    analyze_object_config_manager: AbstractAnalyzeImageConfigManager[ObjectAnalysisConfigRequest, ObjectAnalysisConfigResponse] = Injects("analyze_object_config_manager"),
) -> list[ObjectAnalysisConfigResponse]:
    return await analyze_object_config_manager.get_all_configs(account_id=account_id)

@router.patch(
    path="/object/{configId}",
    summary="Update configuration",
    description="Update configuration for analyzing image for objects",
    status_code=200,
    responses={
        400: {"model": ConfigureBadRequestException.model},
        404: {"model": ConfigureNotFoundException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def update_config(
    configId: UUID,
    request: ObjectAnalysisConfigRequest,
    account_id: UUID = Security(authenticate, scopes=[AuthorizationScopeEnum.CONFIGURE.value]),
    analyze_object_config_manager: AbstractAnalyzeImageConfigManager[ObjectAnalysisConfigRequest, ObjectAnalysisConfigResponse] = Injects("analyze_object_config_manager"),
) -> ObjectAnalysisConfigResponse:
    return await analyze_object_config_manager.update_config(account_id=account_id, config_id=configId, request=request)


@router.delete(
    path="/object/{configId}",
    summary="Delete configuration",
    description="Delete configuration for analyzing image for objects",
    status_code=204,
    responses={
        404: {"model": ConfigureNotFoundException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def delete_config(
    configId: UUID,
    account_id: UUID = Security(authenticate, scopes=[AuthorizationScopeEnum.CONFIGURE.value]),
    analyze_object_config_manager: AbstractAnalyzeImageConfigManager[ObjectAnalysisConfigRequest, ObjectAnalysisConfigResponse] = Injects("analyze_object_config_manager"),
) -> None:
    return await analyze_object_config_manager.delete_config(account_id=account_id, config_id=configId)
# endregion: object