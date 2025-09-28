from pydantic import Field

# local imports
from . import BaseDto


class ImageResolutionDto(BaseDto):
    width: int = Field(title="Image width in pixels")
    height: int = Field(title="Image height in pixels")