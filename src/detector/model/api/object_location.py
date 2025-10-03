from pydantic import Field

from common.model import ResponseBase

# local imports
from ..enum import ObjectEnum
from ..dto import ObjectBoundingBoxDto
from .pixel_coordinate import PixelCoordinate

class ObjectLocationResponse(ResponseBase):
    object_type: ObjectEnum = Field(title="Object type")
    confidence: int = Field(title="Object detection confidence in percentage")
    top_left: PixelCoordinate = Field(title="Top-left corner of bounding box")
    bottom_right: PixelCoordinate = Field(title="Bottom-right corner of bounding box")

    @classmethod
    def from_bounding_box(cls, dto: ObjectBoundingBoxDto) -> 'ObjectLocationResponse':
        return ObjectLocationResponse(
            object_type=dto.object_type,
            confidence=dto.confidence,
            top_left=PixelCoordinate.from_dto(dto.top_left),
            bottom_right=PixelCoordinate.from_dto(dto.bottom_right)
        )
    
    @classmethod
    def to_bounding_box(cls, model: 'ObjectLocationResponse') -> ObjectBoundingBoxDto:
        return ObjectBoundingBoxDto(
            object_type=model.object_type,
            confidence=model.confidence,
            top_left=PixelCoordinate.to_dto(model.top_left),
            bottom_right=PixelCoordinate.to_dto(model.bottom_right)
        )
