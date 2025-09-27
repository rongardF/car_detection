from uuid import UUID
from fastapi import APIRouter, Depends

from common import Injects

# local imports
from ...authentication import authenticate, get_password_hash
from ...doc import Tags
from ...database import UserRepository, JWTRepository, APIKeyRepository
from ...model.api import UserResponse, UserRequest
from ...exception import AnalyzerException, AccountBadRequestException, AccountNotFoundException, AccountUnAuthorizedException

router = APIRouter(tags=[Tags.ACCOUNT], prefix="/v1/user")


@router.post(
    path="/",
    summary="Add user",
    description="Create new user account",
    status_code=200,
    responses={
        400: {"model": AccountBadRequestException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def add_user(
    request: UserRequest,
    user_repository: UserRepository = Injects("user_repository"),
) -> UserResponse:
    pass_hash = get_password_hash(request.password)
    return await user_repository.create(
        values={
            "first_name": request.first_name,
            "last_name": request.last_name,
            "email": request.email,
            "phone": request.phone,
            "hashed_password": pass_hash,
        }
    )


@router.get(
    path="/",
    summary="Get user",
    description="Get user account info",
    status_code=200,
    responses={
        404: {"model": AccountNotFoundException.model},
        401: {"model": AccountUnAuthorizedException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def get_user(
    user_id: UUID = Depends(authenticate),
    user_repository: UserRepository = Injects("user_repository"),
) -> UserResponse:
    return await user_repository.get_one(entity_id=user_id)


@router.patch(
    path="/",
    summary="Update user",
    description="Update user account data",
    status_code=200,
    responses={
        400: {"model": AccountBadRequestException.model},
        401: {"model": AccountUnAuthorizedException.model},
        404: {"model": AccountNotFoundException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def update_user(
    request: UserRequest,
    user_id: UUID = Depends(authenticate),
    user_repository: UserRepository = Injects("user_repository"),
) -> UserResponse:
    return await user_repository.update(
        entity_id=user_id,
        values={
            "first_name": request.first_name,
            "last_name": request.last_name,
            "email": request.email,
            "phone": request.phone
        }
    )


@router.delete(
    path="/",
    summary="Delete user",
    description="Delete user account",
    status_code=204,
    responses={
        401: {"model": AccountUnAuthorizedException.model},
        404: {"model": AccountNotFoundException.model},
        500: {"model": AnalyzerException.model},
    },
)
async def delete_user(
    user_id: UUID = Depends(authenticate),
    user_repository: UserRepository = Injects("user_repository"),
    jwt_repository: JWTRepository = Injects("jwt_repository"),
    api_key_repository: APIKeyRepository = Injects("api_key_repository"),
) -> None:
    # delete keys and invalidate access
    await api_key_repository.delete_by_user_id(user_id=user_id)
    await jwt_repository.delete_by_user_id(user_id=user_id)
    # delete the actual user entity
    return await user_repository.delete(entity_id=user_id)