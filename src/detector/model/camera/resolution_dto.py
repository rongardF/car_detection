from pydantic import BaseModel, ConfigDict, Field


class ResolutionDto(BaseModel):
    model_config = ConfigDict(frozen=True)

    width: int = Field(description="Width of the image.")
    height: int = Field(description="Height of the image.")