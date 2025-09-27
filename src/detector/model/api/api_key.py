from uuid import UUID
from pydantic import Field

from common.model import ResponseBase


class APIKeyResponse(ResponseBase):
    id: UUID = Field(title="Key ID", description="Unique entity identifier for API key")
    key: str = Field(title="API key", description="API key in un-encrypted form")