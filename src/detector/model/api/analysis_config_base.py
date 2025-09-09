from typing import Optional
from uuid import UUID
from pydantic import Field

from common.model import RequestBase, ResponseBase

# local imports
from .image_resolution import ImageResolution
from .pixel_coordinate import PixelCoordinate

BASE_CONFIDENCE = 0.85

class AnalysisConfigBaseRequest(RequestBase):
    confidence: float = Field(title="Confidence threshold", description="Confidence level above which detected object is trusted to be correct (0...1.0)", default=BASE_CONFIDENCE)
    image_resolution: ImageResolution = Field(title="Image resolution")
    image_mask: Optional[list[PixelCoordinate]] = Field(title="Image mask", description="Area on the image that will be blacked out before analysis", default=None)


class AnalysisConfigBaseResponse(ResponseBase):
    confidence: float = Field(title="Confidence threshold", description="Confidence level above which detected object is trusted to be correct (0...1.0)", default=BASE_CONFIDENCE)
    id: UUID = Field(title="Analysis config ID")
    image_resolution: ImageResolution = Field(title="Image resolution")
    image_mask: Optional[list[PixelCoordinate]] = Field(title="Image mask", description="Area on the image that will be blacked out before analysis", default=None)
