from pydantic import Field

# local imports
from . import BaseDto


class BlobFileContainerDto(BaseDto):
    blob_path: str = Field(title="Blob storage path to file")
    data: bytes = Field(title="Data in binary format")