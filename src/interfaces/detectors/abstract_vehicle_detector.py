from abc import abstractmethod, ABC
from PIL.ImageFile import ImageFile

from src.models import DetectionDto


class AbstractVehicleDetector(ABC):

    @abstractmethod
    def detect_and_count(self, image: ImageFile) -> DetectionDto:
        raise NotImplementedError()