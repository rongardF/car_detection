from pydantic import Field

# local imports
from . import BaseDto


class PixelCoordinateDto(BaseDto):
    width: int = Field(title="Pixel number in width")
    height: int = Field(title="Pixel number in height")