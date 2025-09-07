from pydantic import Field

from common.model import ResponseBase


class PixelCoordinate(ResponseBase):
    width: int = Field(title="Pixel number in width")
    height: int = Field(title="Pixel number in height")