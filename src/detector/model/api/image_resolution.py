from pydantic import Field

from common.model import RequestBase


class ImageResolution(RequestBase):
    width: int = Field(title="Image width in pixels", default=1920)
    height: int = Field(title="Image height in pixels", default=1080)