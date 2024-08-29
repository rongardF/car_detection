from PIL import Image
from pydantic import BaseModel, ConfigDict

from src.models.camera import ParametersDto


class Payload(BaseModel):  # TODO: make this model which Flask will generate automatically based on request body
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    parameters: ParametersDto
    image: str