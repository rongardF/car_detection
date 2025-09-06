from typing import Optional
from uuid import UUID
from pydantic import Field

from common.model import RequestBase, ResponseBase

# local imports
from .image_resolution import ImageResolution
from ...detector import PixelCoordinate


class AnalysisConfigBaseRequest(RequestBase):
    image_resolution: ImageResolution = Field(title="Image resolution")
    image_mask: Optional[list[PixelCoordinate]] = Field(title="Image mask", description="Area on the image that will be blacked out before analysis", default=None)


class AnalysisConfigBaseResponse(ResponseBase):
    id: UUID = Field(title="Analysis config ID")
    image_resolution: ImageResolution = Field(title="Image resolution")
    image_mask: Optional[list[PixelCoordinate]] = Field(title="Image mask", description="Area on the image that will be blacked out before analysis", default=None)
    

