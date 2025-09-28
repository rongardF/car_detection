from abc import ABC, abstractmethod
from fastapi import UploadFile

from ...model.api import ObjectCountResponse, CountAnalysisConfigResponse


class AbstractObjectCounter(ABC):

    @abstractmethod
    async def count(self, file: UploadFile, count_analysis: CountAnalysisConfigResponse) -> ObjectCountResponse:
        raise NotImplementedError()