from pydantic import Field

# local imports
from . import BaseDto
from ..enum import ObjectEnum
from .pixel_coordinate_dto import PixelCoordinateDto


class ObjectBoundingBoxDto(BaseDto):
    object_type: ObjectEnum = Field(title="Object type")
    confidence: int = Field(title="Object detection confidence in percentage")
    top_left: PixelCoordinateDto = Field(title="Top-left corner of bounding box")
    bottom_right: PixelCoordinateDto = Field(title="Bottom-right corner of bounding box")
