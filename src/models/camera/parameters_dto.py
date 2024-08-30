from typing import List
from pydantic import BaseModel, ConfigDict, Field

from src.models.camera import ResolutionDto


class ParametersDto(BaseModel):
    model_config = ConfigDict(frozen=True)

    resolution: ResolutionDto = Field(
        description="Resolution of the provided image for preocessing."
    )
    blackout_mask: List[List[float]] = Field(
        description=(
            "Pixel coordinates of the are on the provided image "
            "that will be converted to black pixels (not processed). This "
            "will be the are aof the image where objects (vechicles) should not "
            "be included."
        )
    )
    return_inferred_image: bool = Field(
        description=(
            "If set then processed image will be returned in response body."
        )
    )
    include_boundary_boxes: bool = Field(
        description=(
            "If set then processed image will include boundary boxes for "
            "detected objects (vechicles)."
        )
    )
    include_confidence: bool= Field(
        description=(
            "If set then processed image will include confidence level for "
            "detected objects (vechicles)."
        )
    )