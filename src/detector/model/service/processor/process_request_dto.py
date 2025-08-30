from pydantic import BaseModel, ConfigDict, Field

# local imports
from ...camera import ParametersDto


class ProcessRequestDto(BaseModel):
    """
    Data object containing processing request data.
    """
    model_config = ConfigDict(
        frozen=True, 
        arbitrary_types_allowed=True
    )

    parameters: ParametersDto = Field(
        description="Processing request parameters."
    )
    image_base64: str = Field("Image to be processed in 'base64' encoding")