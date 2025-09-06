from abc import ABC, abstractmethod
from fastapi import UploadFile

from ...model.api import VehicleCountResponse, CountAnalysisConfigResponse


class AbstractVehicleCounter(ABC):

    @abstractmethod
    async def count(self, file: UploadFile, count_analysis: CountAnalysisConfigResponse) -> VehicleCountResponse:
        raise NotImplementedError()