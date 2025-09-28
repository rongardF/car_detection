from datetime import datetime, timedelta, timezone
from uuid import UUID
from typing import Optional

from jwt import encode, decode
from jwt.exceptions import InvalidTokenError
from fastapi import Security, Depends
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from passlib.context import CryptContext

from common import Config
from common.exception.repository_exception import NotFoundException

# local imports
from ..database import APIKeyRepository
from ..exception.api import AccountUnAuthorizedException

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="generate_token", refreshUrl="refresh_token", auto_error=False)


class AuthenticationManager():

    def __init__(self, config: Config, api_key_repository: APIKeyRepository):
        # self._access_token_secret_key = config.require_config("ACCESS_TOKEN_SECRET_KEY")
        # self._refresh_token_secret_key = config.require_config("REFRESH_TOKEN_SECRET_KEY")
        # self._algorithm = config.require_config("JWT_ALGORITHM")

        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        self._api_key_repository = api_key_repository

    async def authenticate(
        self,
        api_key: Security = Security(api_key_header),
        token: Depends = Depends(oauth2_scheme),
    ) -> UUID:
        if api_key:
            try:
                api_key_entity = await self._api_key_repository.get_one(entity_id=UUID(api_key))
                return api_key_entity.user_id
            except NotFoundException:
                raise AccountUnAuthorizedException()
            
        if token:
            return self.verify_token(token=token)
        
        # if no authentication method hit then un-authorized
        raise AccountUnAuthorizedException()
    
    def get_password_hash(self, password: str) -> str:
        return self._pwd_context.hash(password)


    def password_hash_match(self, plain_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)


    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:  # default expiry is 15 minutes
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = encode(to_encode, self._access_token_secret_key, algorithm=self._algorithm)
        return encoded_jwt


    def create_refresh_token(self, data: dict, expires_delta: timedelta | None = None):
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
        else:  # default expiry is 15 minutes
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)  # FIXME: expiry must be longer here because we don't generate new refresh tokens - this single token will be used to refresh access token until it expiry in whcih case we force the user to login again
        to_encode.update({"exp": expire})
        encoded_jwt = encode(to_encode, self._refresh_token_secret_key, algorithm=self._algorithm)
        return encoded_jwt


    def verify_token(self, token: str, type: str = "access") -> UUID:
        try:
            if type == "access":
                secret_key = self._access_token_secret_key
            else:
                secret_key = self._refresh_token_secret_key

            payload: dict = decode(token, secret_key, algorithms=[self._algorithm])
            user_id = payload.get("sub")
            if user_id is None:
                raise AccountUnAuthorizedException()
        except InvalidTokenError:
            raise AccountUnAuthorizedException()

        return user_id
