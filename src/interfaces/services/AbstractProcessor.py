from typing import Dict, Any, Tuple
from abc import ABC, abstractmethod

from src.models import ProcessRequestDto, ProcessResultDto


class AbstractProcessor(ABC):

    @abstractmethod
    def process(self, process_request: ProcessRequestDto) -> ProcessResultDto:
        raise NotImplementedError()