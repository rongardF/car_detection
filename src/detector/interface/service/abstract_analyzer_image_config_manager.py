from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from ...model.api import ImageAnalysisConfigBaseRequest, ImageAnalysisConfigBaseResponse

REQUEST = TypeVar("REQUEST", bound=ImageAnalysisConfigBaseRequest)
RESPONSE = TypeVar("RESPONSE", bound=ImageAnalysisConfigBaseResponse)


class AbstractAnalyzeImageConfigManager(ABC, Generic[REQUEST, RESPONSE]):

    @abstractmethod
    async def add_config(self, account_id: UUID, request: REQUEST) -> RESPONSE:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_config(self, account_id: UUID, config_id: UUID) -> RESPONSE:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_all_configs(self, account_id: UUID) -> RESPONSE:
        raise NotImplementedError()
    
    @abstractmethod
    async def update_config(self, account_id: UUID, config_id: UUID, request: REQUEST) -> RESPONSE:
        raise NotImplementedError()
    
    @abstractmethod
    async def delete_config(self, account_id: UUID, config_id: UUID) -> None:
        raise NotImplementedError()