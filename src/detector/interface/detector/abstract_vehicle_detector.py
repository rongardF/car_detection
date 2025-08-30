from abc import abstractmethod, ABC

from ...model import DetectionRequestDto, DetectionResultDto


class AbstractVehicleDetector(ABC):

    @abstractmethod
    def detect_and_count(
        self, detection_request: DetectionRequestDto
    ) -> DetectionResultDto:
        raise NotImplementedError()