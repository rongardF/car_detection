from PIL import Image
from pydantic import BaseModel, ConfigDict

from src.models.camera import ParametersDto


class DetectionRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True, 
        arbitrary_types_allowed=True
    )

    parameters: ParametersDto
    image_base64: str