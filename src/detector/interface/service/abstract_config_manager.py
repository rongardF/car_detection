from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from ...model.api import AnalysisConfigBaseRequest, AnalysisConfigBaseResponse

REQUEST = TypeVar("REQUEST", bound=AnalysisConfigBaseRequest)
RESPONSE = TypeVar("RESPONSE", bound=AnalysisConfigBaseResponse)


class AbstractAnalyzeConfigManager(ABC, Generic[REQUEST, RESPONSE]):

    @abstractmethod
    async def add_config(self, user_id: UUID, request: REQUEST) -> RESPONSE:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_config(self, user_id: UUID, config_id: UUID) -> RESPONSE:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_all_configs(self, user_id: UUID) -> RESPONSE:
        raise NotImplementedError()
    
    @abstractmethod
    async def update_config(self, user_id: UUID, config_id: UUID, request: REQUEST) -> RESPONSE:
        raise NotImplementedError()
    
    @abstractmethod
    async def delete_config(self, user_id: UUID, config_id: UUID) -> None:
        raise NotImplementedError()