from pydantic import Field

# local imports
from ..enum import ObjectEnum
from .analyze_config_base_dto import AnalyzeConfigBaseDto


class AnalyzeObjectCountConfigDto(AnalyzeConfigBaseDto):
    objects: list[ObjectEnum] = Field(title="Objects to count on the image")
