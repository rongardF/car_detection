from typing import Optional
from abc import abstractmethod, ABC
from numpy import ndarray

# local imports
from ...model.enum import ObjectEnum
from ...model.detector import ObjectBoundingBox


class AbstractObjectDetector(ABC):

    @abstractmethod
    def count(self, image: ndarray, objects: list[ObjectEnum], confidence: Optional[int] = None) -> dict[ObjectEnum, int]:
        raise NotImplementedError()
    
    @abstractmethod
    def detect(self, image: ndarray, objects: list[ObjectEnum], confidence: Optional[int] = None) -> dict[ObjectEnum, list[ObjectBoundingBox]]:
        raise NotImplementedError()