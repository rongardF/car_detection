from pydantic import Field

# local imports
from ..enum import ObjectEnum
from .image_analysis_config_base import ImageAnalysisConfigBaseRequest, ImageAnalysisConfigBaseResponse

BASE_CONFIDENCE = 0.85


class ObjectAnalysisConfigRequest(ImageAnalysisConfigBaseRequest):
    confidence: float = Field(title="Confidence threshold", description="Confidence level above which detected object is trusted to be correct (0...1.0)", default=BASE_CONFIDENCE)
    objects: list[ObjectEnum] = Field(title="Objects of interest on the image")


class ObjectAnalysisConfigResponse(ImageAnalysisConfigBaseResponse):
    confidence: float = Field(title="Confidence threshold", description="Confidence level above which detected object is trusted to be correct (0...1.0)", default=BASE_CONFIDENCE)
    objects: list[ObjectEnum] = Field(title="Objects of interest on the image")
