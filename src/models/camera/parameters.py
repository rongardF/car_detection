from typing import List
from pydantic import BaseModel, ConfigDict

from src.models.camera import ResolutionDto


class ParametersDto(BaseModel):
    model_config = ConfigDict(frozen=True)

    location_id: str
    resolution: ResolutionDto
    blackout_mask: List[List[float]]