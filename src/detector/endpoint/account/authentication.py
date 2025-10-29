from uuid import UUID
from typing import Annotated

from cryptography.fernet import Fernet
from fastapi import APIRouter, Security, Depends
from fastapi.security import OAuth2PasswordRequestForm

from common import Injects
from common.exception.repository_exception import NotFoundException

# local imports
from ...authentication import authenticate, password_hash_match, create_access_token, create_refresh_token, verify_token, generate_api_key, get_api_key_hash
from ...doc import Tags
from ...database import APIKeyRepository, AccountRepository, JWTRepository
from ...model.enum import AuthorizationScopeEnum
from ...model.api import APIKeyResponse, AccessTokenResponse, RefreshTokenRequest
from ...exception import AnalyzerException, AccountBadRequestException, AccountNotFoundException, AccountUnAuthorizedException

router = APIRouter(tags=[Tags.ACCOUNT], prefix="/v1/account/authentication")


# region: api-key
@router.post(
    path="/generate_key",
    summary="New API key",
    description="Generate new API key",
    status_code=200,
    responses={
        400: {"model": AccountBadRequestException.model},
        401: {"model": AccountUnAuthorizedException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def generate_key(
    account_id: UUID = Security(authenticate, scopes=[AuthorizationScopeEnum.ACCOUNT.value]),
    api_key_repository: APIKeyRepository = Injects("api_key_repository"),
    cipher: Fernet = Injects("cipher"),
) -> APIKeyResponse:
    key = generate_api_key()
    encrypted_key = cipher.encrypt(key.encode())
    hashed_key = get_api_key_hash(key)
    api_key = await api_key_repository.create(
        values={
            "account_id": account_id,
            "hashed_key": hashed_key,
            "scopes": AuthorizationScopeEnum.ANALYZE.value,
            "encrypted_key": encrypted_key
        }
    )

    return APIKeyResponse(
        id=api_key.id,
        key=key,
    )


@router.get(
    path="/get_keys",
    summary="Get API keys",
    description="Get API keys for user account",
    status_code=200,
    responses={
        401: {"model": AccountUnAuthorizedException.model},
        404: {"model": AccountNotFoundException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def get_keys(
    account_id: UUID = Security(authenticate, scopes=[AuthorizationScopeEnum.ACCOUNT.value]),
    api_key_repository: APIKeyRepository = Injects("api_key_repository"),
    cipher: Fernet = Injects("cipher"),
) -> list[APIKeyResponse]:
    api_key_entities = await api_key_repository.get_by_account_id(account_id=account_id)
    return [
        APIKeyResponse(id=key.id,key=cipher.decrypt(key.encrypted_key).decode())
        for key in api_key_entities
    ]


@router.delete(
    path="/delete_key",
    summary="Delete API key",
    description="Delete API keys for user account",
    status_code=204,
    responses={
        401: {"model": AccountUnAuthorizedException.model},
        404: {"model": AccountNotFoundException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def delete_key(
    api_key_uuid: UUID,
    account_id: UUID = Security(authenticate, scopes=[AuthorizationScopeEnum.ACCOUNT.value]),
    api_key_repository: APIKeyRepository = Injects("api_key_repository"),
) -> None:
    try:
        return await api_key_repository.delete_with_account_id(entity_id=api_key_uuid, account_id=account_id)
    except NotFoundException:
        raise AccountBadRequestException()
# endregion: api-key

# region: token
@router.post(
    path="/generate_token",
    summary="Get token",
    description="Get new access token (login)",
    status_code=200,
    responses={
        400: {"model": AccountBadRequestException.model},
        401: {"model": AccountUnAuthorizedException.model},
        404: {"model": AccountNotFoundException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def generate_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    account_repository: AccountRepository = Injects("account_repository"),
    jwt_repository: JWTRepository = Injects("jwt_repository")
) -> AccessTokenResponse:
    try:
        account_entities = await account_repository.get_by_email(email=form_data.username)
    except NotFoundException:
        raise AccountUnAuthorizedException()
    
    if len(account_entities) == 0:
        raise AccountNotFoundException()
    if len(account_entities) != 1:
        # there cannot be more than one account with this email!
        raise AnalyzerException()  # FIXME: make this custom exception
    else:
        account_entity = account_entities[0]

    if not password_hash_match(form_data.password, account_entity.hashed_password):
        raise AccountUnAuthorizedException()
    
    # NOTE: only one device can be logged in at any given time because we
    # clear the repository for the account per each login
    await jwt_repository.delete_by_account_id(account_id=account_entity.id)
    
    access_token = create_access_token(
        data={"sub": str(account_entity.id)}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(account_entity.id)}
    )

    jwt_entity = await jwt_repository.create(
        values={
            "account_id": account_entity.id,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )

    return AccessTokenResponse(
        access_token=jwt_entity.access_token,
        refresh_token=jwt_entity.refresh_token,
    )


@router.post(
    path="/refresh_token",
    summary="Refresh token",
    description="Refresh the access token",
    status_code=200,
    responses={
        400: {"model": AccountBadRequestException.model},
        401: {"model": AccountUnAuthorizedException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def refresh_token(
    request: RefreshTokenRequest,
    authenticated_account_id: UUID = Security(authenticate, scopes=[AuthorizationScopeEnum.ACCOUNT.value]),
    jwt_repository: JWTRepository = Injects("jwt_repository")
) -> AccessTokenResponse:
    account_id = verify_token(token=request.refresh_token, type="refresh")
    if authenticated_account_id != account_id:
        raise AccountUnAuthorizedException()

    # because refresh token is generated by us then it is guaranteed
    # that account ID is valid and not corrupted - we don't need to fetch account model again

    access_token = create_access_token(
        data={"sub": str(account_id)}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(account_id)}
    )

    jwt_entities = await jwt_repository.update_by_account_id(
        account_id=account_id,
        values={
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )

    if len(jwt_entities) != 1:
        # there cannot be more than one JWT entity per account!
        raise AnalyzerException()  # FIXME: make this custom exception
    else:
        jwt_entity = jwt_entities[0]

    return AccessTokenResponse(
        access_token=jwt_entity.access_token,
        refresh_toke=jwt_entity.refresh_token,
    )


@router.post(
    path="/terminate_token",
    summary="Terminate token",
    description="Invalidate refresh and access token (logout)",
    status_code=204,
    responses={
        400: {"model": AccountBadRequestException.model},
        401: {"model": AccountUnAuthorizedException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def terminate_token(
    account_id: UUID = Security(authenticate, scopes=[AuthorizationScopeEnum.ACCOUNT.value]),
    jwt_repository: JWTRepository = Injects("jwt_repository")
) -> None:
    await jwt_repository.delete_by_account_id(account_id=account_id)
# endregion: token