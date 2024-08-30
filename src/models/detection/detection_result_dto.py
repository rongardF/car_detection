import numpy as np
from pydantic import BaseModel, ConfigDict, Field
from PIL import Image

from src.models.detection.detection_request_dto import DetectionRequestDto


class DetectionResultDto(BaseModel):
    """
    Data object containing processed image and data.
    """
    model_config = ConfigDict(
        frozen=True, 
        arbitrary_types_allowed=True
    )
    
    detection_request: DetectionRequestDto
    inferred_image: Image = Field(
        description=(
            "Image with detection data (location, confidence, etc.) data "
            "overlayed if it was enabled in request parameters."
        )
    )
    boundary_boxes: np.ndarray = Field(
        description=(
            "Detected objects (vechicles) boundary boxes pixel coordinates "
            "(each box is specified with top-left and bottom-right coordinates)."
        )
    )
    count: int = Field(description="Number of objects (vechicles) detected.")