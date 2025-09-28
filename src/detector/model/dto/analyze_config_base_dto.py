from typing import Optional
from uuid import UUID
from pydantic import Field

# local imports
from . import BaseDto
from .image_resolution_dto import ImageResolutionDto
from .pixel_coordinate_dto import PixelCoordinateDto


class AnalyzeConfigBaseDto(BaseDto):
    id: Optional[UUID] = Field(title="Configuration identification")
    image_resolution: ImageResolutionDto = Field(title="Image resolution")
    image_mask: Optional[list[PixelCoordinateDto]] = Field(title="Image mask", description="Area on the image that will be blacked out before analysis", default=None)
