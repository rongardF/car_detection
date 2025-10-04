from abc import ABC, abstractmethod
from fastapi import UploadFile

from ...model.api import ObjectCountResponse, ObjectLocationResponse, ObjectAnalysisConfigResponse


class AbstractImageAnalyzer(ABC):

    @abstractmethod
    async def count_objects(self, file: UploadFile, object_analysis_config: ObjectAnalysisConfigResponse) -> list[ObjectCountResponse]:
        raise NotImplementedError()
    
    @abstractmethod
    async def locate_objects(self, file: UploadFile, object_analysis_config: ObjectAnalysisConfigResponse) -> list[ObjectLocationResponse]:
        raise NotImplementedError()