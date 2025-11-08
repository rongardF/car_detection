from typing import Annotated
from fastapi import APIRouter, Security, Response, UploadFile, File
from uuid import UUID, uuid4

from common import Injects

# local imports
from ...authentication import authenticate
from ...doc import Tags
from ...model.enum import AuthorizationScopeEnum
from ...interface import AbstractAnalyzeImageConfigManager, AbstractImageProcessor, AbstractFileStorage
from ...model.api import ObjectAnalysisConfigRequest, ObjectAnalysisConfigResponse, FileUploadResponse
from ...model.dto import FileContainerDto
from ...exception import AnalyzerException, FileNotFound, ConfigureImageNotFoundException, ConfigureBadRequestException, ConfigureEntityNotFoundException, AccountUnAuthorizedException

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
        401: {"model": AccountUnAuthorizedException.model},
        404: {"model": ConfigureEntityNotFoundException.model},
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
        401: {"model": AccountUnAuthorizedException.model},
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
        401: {"model": AccountUnAuthorizedException.model},
        404: {"model": ConfigureEntityNotFoundException.model},
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
    description="Delete configuration for analyzing image for objects. Also deletes example image file.",
    status_code=204,
    responses={
        401: {"model": AccountUnAuthorizedException.model},
        404: {"model": ConfigureEntityNotFoundException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def delete_config(
    configId: UUID,
    account_id: UUID = Security(authenticate, scopes=[AuthorizationScopeEnum.CONFIGURE.value]),
    analyze_object_config_manager: AbstractAnalyzeImageConfigManager[ObjectAnalysisConfigRequest, ObjectAnalysisConfigResponse] = Injects("analyze_object_config_manager"),
    file_storage: AbstractFileStorage = Injects("file_storage"),
) -> None:
    # delete image file
    config = await analyze_object_config_manager.get_config(account_id=account_id, config_id=configId)
    try:
        await file_storage.delete_file(account_id=account_id, file_id=config.example_image_id)
    except FileNotFound:
        pass  # TODO: log this as warning
    # delete config
    return await analyze_object_config_manager.delete_config(account_id=account_id, config_id=configId)
# endregion: object


# region: image
@router.post(
    path="/image",
    summary="Upload configuration image",
    description="Upload a configuration image to storage. Supported formats: jpg, jpeg, png.",
    status_code=200,
    responses={
        400: {"model": ConfigureBadRequestException.model},
        401: {"model": AccountUnAuthorizedException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def upload(
    file: Annotated[UploadFile, File(title="Uploaded file")],
    account_id: UUID = Security(authenticate, scopes=[AuthorizationScopeEnum.CONFIGURE.value]),
    image_processor: AbstractImageProcessor = Injects("image_processor"),
    file_storage: AbstractFileStorage = Injects("file_storage"),
) -> FileUploadResponse:
    if not image_processor.is_allowed_type(file=file):
        raise ConfigureBadRequestException()
    
    data = await file.read()
    suffix = image_processor.get_image_type(file=file)

    file_container = FileContainerDto(
        file_id=uuid4(),
        data_format=suffix,
        data=data
    )
    stored_file_id = await file_storage.store_file(account_id=account_id, file=file_container)

    return FileUploadResponse(file_id=stored_file_id)


@router.get(
    path="/image/{fileId}",
    summary="Download image",
    description="Download configuration image from storage. Supported formats: jpg, jpeg, png.",
    status_code=200,
    responses={
        401: {"model": AccountUnAuthorizedException.model},
        404: {"model": ConfigureImageNotFoundException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def download(
    fileId: UUID,
    account_id: UUID = Security(authenticate, scopes=[AuthorizationScopeEnum.CONFIGURE.value]),
    file_storage: AbstractFileStorage = Injects("file_storage"),
) -> Response:
    try:
        file_container = await file_storage.fetch_file(account_id=account_id, file_id=fileId)
    except FileNotFound:
        raise ConfigureImageNotFoundException()
    
    if file_container.data_format in ("jpg", "jpeg"):
        media_type = "image/jpeg"
    elif file_container.data_format in ("png"):
        media_type = "image/png"
    else:
        raise ValueError("not_allowed_file_type")

    return Response(
        content=file_container.data,
        media_type=media_type,
    )

@router.delete(
    path="/image/{fileId}",
    summary="Delete image",
    description="Delete configuration image from storage",
    status_code=204,
    responses={
        401: {"model": AccountUnAuthorizedException.model},
        404: {"model": ConfigureImageNotFoundException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def download(
    fileId: UUID,
    account_id: UUID = Security(authenticate, scopes=[AuthorizationScopeEnum.CONFIGURE.value]),
    file_storage: AbstractFileStorage = Injects("file_storage"),
) -> None:
    try:
        await file_storage.delete_file(account_id=account_id, file_id=fileId)
    except FileNotFound:
        raise ConfigureImageNotFoundException()
# endregion: image