import numpy as np
from pydantic import BaseModel, ConfigDict, Field
from PIL import Image

from src.models.services.processor.process_request_dto import ProcessRequestDto


class DetectionRequestDto(BaseModel):
    """
    Data object containing data for performing detection.
    """
    model_config = ConfigDict(
        frozen=True, 
        arbitrary_types_allowed=True
    )
    
    process_request: ProcessRequestDto = Field(
        description="Processing request data."
    )
    image: Image = Field(
        description=(
            "Image where objects (vechicles) detection will be performed."
        )
    )