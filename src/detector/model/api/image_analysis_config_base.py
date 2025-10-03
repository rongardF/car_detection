from typing import Optional
from uuid import UUID
from pydantic import Field

from common.model import RequestBase, ResponseBase

# local imports
from .image_resolution import ImageResolution
from .pixel_coordinate import PixelCoordinate


class ImageAnalysisConfigBaseRequest(RequestBase):
    image_resolution: ImageResolution = Field(title="Image resolution", description="Resolution of the images that will be analyzed")
    image_mask: Optional[list[PixelCoordinate]] = Field(title="Image mask", description="Area on the image that will be blacked out before analysis")


class ImageAnalysisConfigBaseResponse(ResponseBase):
    id: UUID = Field(title="Analysis config ID")
    image_resolution: ImageResolution = Field(title="Image resolution", description="Resolution of the images that will be analyzed")
    image_mask: Optional[list[PixelCoordinate]] = Field(title="Image mask", description="Area on the image that will be blacked out before analysis")
