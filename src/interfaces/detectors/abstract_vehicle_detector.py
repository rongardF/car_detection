from abc import abstractmethod, ABC

from src.models import DetectionRequestDto, DetectionResultDto


class AbstractVehicleDetector(ABC):

    @abstractmethod
    def detect_and_count(
        self, detection_request: DetectionRequestDto
    ) -> DetectionResultDto:
        raise NotImplementedError()