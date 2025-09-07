from typing import Optional
from abc import abstractmethod, ABC
from numpy import ndarray

# local imports
from ...model.enum import ObjectEnum
from ...model.dto import ObjectBoundingBoxDto


class AbstractObjectDetector(ABC):

    @abstractmethod
    def count(self, image: ndarray, objects: list[ObjectEnum], confidence: Optional[int] = None) -> dict[ObjectEnum, int]:
        raise NotImplementedError()
    
    @abstractmethod
    def detect(self, image: ndarray, objects: list[ObjectEnum], confidence: Optional[int] = None) -> dict[ObjectEnum, list[ObjectBoundingBoxDto]]:
        raise NotImplementedError()