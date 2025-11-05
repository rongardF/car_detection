from uuid import UUID
from pydantic import Field

# local imports
from . import BaseDto


class FileContainerDto(BaseDto):
    file_id: UUID = Field(title="File ID in storage")
    data_format: str = Field(title="Data format (file suffix)")
    data: bytes = Field(title="Data in binary format")