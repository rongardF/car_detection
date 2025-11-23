from uuid import UUID
from os import environ
from datetime import datetime, timedelta, timezone
from hashlib import sha256

from secrets import token_urlsafe
from jwt import encode, decode
from jwt.exceptions import InvalidTokenError
from fastapi import Security, Depends
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader, SecurityScopes
from passlib.context import CryptContext

from common import Injects
from common.exception.repository_exception import NotFoundException

# local imports
from .database import APIKeyRepository, JWTRepository
from .exception.api import AccountUnAuthorizedException

ACCESS_SECRET_KEY = environ.get("ACCESS_SECRET_KEY")
REFRESH_SECRET_KEY = environ.get("REFRESH_SECRET_KEY")
ALGORITHM = environ.get("ALGORITHM")
API_KEY_LENGTH = int(environ.get("API_KEY_LENGTH"))

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/account/authentication/generate_token", refreshUrl="/v1/account/authentication/refresh_token", auto_error=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate(
    security_scopes: SecurityScopes,
    api_key: str = Security(api_key_header),
    token: str = Depends(oauth2_scheme),
    api_key_repository: APIKeyRepository = Injects("api_key_repository"),
    jwt_repository: JWTRepository = Injects("jwt_repository"),
) -> UUID:
    if api_key:
        try:
            hashed_key = get_api_key_hash(api_key)
            api_key_entity = await api_key_repository.get_by_hashed_key(hashed_key=hashed_key)
            if security_scopes.scopes:  # if scopes are required, check if the API key has the required scopes
                if not api_key_entity.scopes or not any(scope in api_key_entity.scopes.split(";") for scope in security_scopes.scopes):
                    raise AccountUnAuthorizedException()
            # if scopes are not required, we can use the API key
            return api_key_entity.account_id
        except NotFoundException:
            raise AccountUnAuthorizedException()
        
    if token:
        # check that token has not been invalidated (removed from repository)
        try:
            await jwt_repository.get_by_token_value(token_value=token)
        except NotFoundException:
            raise AccountUnAuthorizedException()
        
        return verify_token(token=token)
    
    # if no authentication method hit then un-authorized
    raise AccountUnAuthorizedException()


def get_api_key_hash(api_key: str) -> str:
    return sha256(api_key.encode()).hexdigest()


def api_key_hash_match(plain_api_key: str, hashed_api_key: str) -> str:
    return get_api_key_hash(plain_api_key) == hashed_api_key


def generate_api_key(length: int = API_KEY_LENGTH) -> str:
    return token_urlsafe(length)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def password_hash_match(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:  # default expiry is 30 minutes
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, ACCESS_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a refresh token
    Args:
        data (dict): data to be encoded
        expires_delta (timedelta | None, optional): expiration time. Defaults to None.
    Returns:
        str: JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:  # default expiry is 60 minutes
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)  # FIXME: expiry must be longer here because we don't generate new refresh tokens - this single token will be used to refresh access token until it expiry in whcih case we force the user to login again
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(
    token: str,
    type: str = "access"
) -> UUID:
    try:
        if type == "access":
            secret_key = ACCESS_SECRET_KEY
        else:
            secret_key = REFRESH_SECRET_KEY

        payload: dict = decode(token, secret_key, algorithms=[ALGORITHM])
        account_id = payload.get("sub")
        if account_id is None:
            raise AccountUnAuthorizedException()
    except InvalidTokenError:
        raise AccountUnAuthorizedException()

    return UUID(account_id)
