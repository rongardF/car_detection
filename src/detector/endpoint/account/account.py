from uuid import UUID
from fastapi import APIRouter, Security

from common import Injects
from common.exception.repository_exception import NotUniqueException

# local imports
from ...authentication import authenticate, get_password_hash
from ...doc import Tags
from ...database import AccountRepository, JWTRepository, APIKeyRepository
from ...interface import AbstractFileStorage, AbstractAnalyzeImageConfigManager
from ...model.enum import AuthorizationScopeEnum
from ...model.api import AccountRequest, AccountResponse, ObjectAnalysisConfigRequest, ObjectAnalysisConfigResponse
from ...exception import AnalyzerException, AccountBadRequestException, AccountEmailRegistered, AccountNotFoundException, AccountUnAuthorizedException

router = APIRouter(tags=[Tags.ACCOUNT], prefix="/v1/account")


@router.post(
    path="/",
    summary="Add account",
    description="Create new account",
    status_code=200,
    responses={
        400: {"model": AccountBadRequestException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def add_account(
    request: AccountRequest,
    account_repository: AccountRepository = Injects("account_repository"),
) -> AccountResponse:
    pass_hash = get_password_hash(request.password)
    try:
        account_entity = await account_repository.create(
            values={
                "organization_name": request.organization_name,
                "email": request.email,
                "phone": request.phone,
                "hashed_password": pass_hash,
            }
        )
    except NotUniqueException:
        raise AccountEmailRegistered()

    return AccountResponse(
        id=account_entity.id,
        organization_name=account_entity.organization_name,
        email=account_entity.email,
        phone=account_entity.phone
    )


@router.get(
    path="/",
    summary="Get account",
    description="Get account info",
    status_code=200,
    responses={
        404: {"model": AccountNotFoundException.model},
        401: {"model": AccountUnAuthorizedException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def get_account(
    account_id: UUID = Security(authenticate, scopes=[AuthorizationScopeEnum.ACCOUNT.value]),
    account_repository: AccountRepository = Injects("account_repository"),
) -> AccountResponse:
    account_entity = await account_repository.get_one(entity_id=account_id)

    return AccountResponse(
        id=account_entity.id,
        organization_name=account_entity.organization_name,
        email=account_entity.email,
        phone=account_entity.phone
    )


@router.patch(
    path="/",
    summary="Update account",
    description="Update account data",
    status_code=200,
    responses={
        400: {"model": AccountBadRequestException.model},
        401: {"model": AccountUnAuthorizedException.model},
        404: {"model": AccountNotFoundException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def update_account(
    request: AccountRequest,
    account_id: UUID = Security(authenticate, scopes=[AuthorizationScopeEnum.ACCOUNT.value]),
    account_repository: AccountRepository = Injects("account_repository"),
) -> AccountResponse:
    account_entity = await account_repository.update(
        entity_id=account_id,
        values={
            "organization_name": request.organization_name,
            "email": request.email,
            "phone": request.phone,
        }
    )

    return AccountResponse(
        id=account_entity.id,
        organization_name=account_entity.organization_name,
        email=account_entity.email,
        phone=account_entity.phone
    )


@router.delete(
    path="/",
    summary="Delete account",
    description="Delete account and related data (configs, files, etc.)",
    status_code=204,
    responses={
        401: {"model": AccountUnAuthorizedException.model},
        404: {"model": AccountNotFoundException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def delete_account(
    account_id: UUID = Security(authenticate, scopes=[AuthorizationScopeEnum.ACCOUNT.value]),
    account_repository: AccountRepository = Injects("account_repository"),
    jwt_repository: JWTRepository = Injects("jwt_repository"),
    api_key_repository: APIKeyRepository = Injects("api_key_repository"),
    file_storage: AbstractFileStorage = Injects("file_storage"),
    analyze_object_config_manager: AbstractAnalyzeImageConfigManager[ObjectAnalysisConfigRequest, ObjectAnalysisConfigResponse] = Injects("analyze_object_config_manager"),
) -> None:
    # delete keys and invalidate access
    await api_key_repository.delete_by_account_id(account_id=account_id)
    await jwt_repository.delete_by_account_id(account_id=account_id)
    # delete blob data
    blob_file_ids = await file_storage.fetch_files_list(account_id=account_id)
    for file_id in blob_file_ids:
        await file_storage.delete_file(account_id=account_id, file_id=file_id)
    # delete all configuration data for account
    configs = await analyze_object_config_manager.get_all_configs(account_id=account_id)
    for config in configs:
        await analyze_object_config_manager.delete_config(account_id=account_id, config_id=config.id)
    # delete the actual user entity
    return await account_repository.delete(entity_id=account_id)