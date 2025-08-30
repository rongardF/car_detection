from abc import ABC, abstractmethod
from PIL.ImageFile import ImageFile

from ...model import ParametersDto


class AbstractImageProcessor(ABC):

    @abstractmethod
    def base64_to_image(self, image_base64: str) -> ImageFile:
        raise NotImplementedError()

    @abstractmethod
    def image_to_base64(self, image: ImageFile) -> str:
        raise NotImplementedError()

    @abstractmethod
    def draw_blackout_mask(self, image: ImageFile, parameters: ParametersDto) -> ImageFile:
       raise NotImplementedError()