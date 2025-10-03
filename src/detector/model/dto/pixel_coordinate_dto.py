from typing import Any
from pydantic import Field, model_validator

# local imports
from . import BaseDto


class PixelCoordinateDto(BaseDto):
    width: int = Field(title="Pixel number in width")
    height: int = Field(title="Pixel number in height")

    @classmethod
    @model_validator(mode="before")
    def before_validator(cls, data: Any) -> Any:
        # allow creating an object from tuple with length 2
        if isinstance(data, tuple):
            if len(data) != 2:
                raise ValueError("Tuple length must be 2!")

            if (
                not isinstance(data[0], int) or
                not isinstance(data[1], int)
            ):
                raise ValueError("Tuple elements must be of integer type!")
        
            return PixelCoordinateDto(
                width=data[0],
                height=data[1]
            )
        
        # if not tuple then continue validation pipeline normally
        return data