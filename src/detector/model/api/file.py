from typing import Optional
from uuid import UUID
from pydantic import Field

from common.model import ResponseBase


class FileUploadResponse(ResponseBase):
    file_id: UUID = Field(title="File ID", description="Uploaded file ID for fetching")