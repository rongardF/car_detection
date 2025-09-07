from typing import Any
from pydantic import Field, field_validator

# local imports
from . import BaseDto
from ..enum import ObjectEnum
from .pixel_coordinate_dto import PixelCoordinateDto


class ObjectBoundingBoxDto(BaseDto):
    object_type: ObjectEnum = Field(title="Object type")
    confidence: int = Field(title="Object detection confidence in percentage")
    top_left: PixelCoordinateDto = Field(title="Top-left corner of bounding box")
    bottom_right: PixelCoordinateDto = Field(title="Bottom-right corner of bounding box")

    @classmethod
    def _validate_is_pixel_coordinate(cls, data: Any) -> None:
        if isinstance(data, tuple):
            if len(data) != 2:
                raise ValueError("Tuple length must be 2!")

            if (
                not isinstance(data[0], int) or
                not isinstance(data[0], int)
            ):
                raise ValueError("Tuple elements must be of integer type!")
            
    @classmethod
    @field_validator("top_left", mode="before")
    def before_validator(cls, data: Any) -> Any:
        cls._validate_is_pixel_coordinate(data)
        
        return PixelCoordinateDto(
            width=data[0],
            height=data[1]
        )
        
    @classmethod
    @field_validator("bottom_right", mode="before")
    def before_validator(cls, data: Any) -> Any:
        cls._validate_is_pixel_coordinate(data)
            
        return PixelCoordinateDto(
            width=data[0],
            height=data[1]
        )