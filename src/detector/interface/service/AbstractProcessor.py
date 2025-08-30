from abc import ABC, abstractmethod

from ...model import ProcessRequestDto, ProcessResultDto


class AbstractProcessor(ABC):

    @abstractmethod
    def process(self, process_request: ProcessRequestDto) -> ProcessResultDto:
        raise NotImplementedError()