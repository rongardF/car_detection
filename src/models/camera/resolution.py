from pydantic import BaseModel, ConfigDict


class ResolutionDto(BaseModel):
    model_config = ConfigDict(frozen=True)

    width: int
    height: int