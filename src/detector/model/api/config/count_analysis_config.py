from uuid import UUID
from pydantic import Field

# local imports
from ...enum import ObjectEnum
from .analysis_config_base import AnalysisConfigBaseRequest, AnalysisConfigBaseResponse


class CountAnalysisConfigRequest(AnalysisConfigBaseRequest):
    objects: list[ObjectEnum] = Field(title="Objects to count on the image")


class CountAnalysisConfigResponse(AnalysisConfigBaseResponse):
    objects: list[ObjectEnum] = Field(title="Objects to count on the image")
    

