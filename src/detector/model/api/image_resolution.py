from pydantic import Field

from common.model import RequestBase


class ImageResolution(RequestBase):
    width: int = Field(title="Image width in pixels")
    height: int = Field(title="Image height in pixels")