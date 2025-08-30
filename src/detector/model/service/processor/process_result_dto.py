from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from ...detection.detection_result_dto import DetectionResultDto
from ...detection.detection_request_dto import ProcessRequestDto


class ProcessResultDto(BaseModel):
    """
    Data object containing processed request result data.
    """
    model_config = ConfigDict(
        frozen=True, 
        arbitrary_types_allowed=True
    )

    process_request: ProcessRequestDto = Field(
        description="Processing request data."
    )
    detection_result: DetectionResultDto = Field(
        description="Object (vechicle) detection result data."
    )
    inferred_image_base64: Optional[str] = Field(
        description=(
            "Image with detected objects (vechicles) detection data "
            "(location, confidence etc.) overlayed. Image is in 'base64' "
            "encoding. If returning this image is disabled in request "
            "parameters then this will be NULL (None)."
        )
    ) 