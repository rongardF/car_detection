from pydantic import BaseModel
from pydantic import Field

from common.model import RequestBase, ResponseBase


class AccessTokenResponse(BaseModel):
    access_token: str = Field(title="Access token", alias="access_token")  # swagger UI requires to have them snake_case
    refresh_token: str = Field(title="Refresh token", alias="refresh_token")
    token_type: str = Field(title="Token type", description="Access token type", default="bearer", alias="token_type")


class RefreshTokenRequest(RequestBase):
    refresh_token: str = Field(title="Refresh token", alias="refresh_token")