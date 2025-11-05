from abc import ABC, abstractmethod
from numpy import ndarray
from fastapi import UploadFile

# local imports
from ...model.dto import ImageResolutionDto
from ...model.api import ObjectLocationResponse


class AbstractImageProcessor(ABC):

    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
    ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}

    @abstractmethod
    def is_allowed_type(self, file: UploadFile) -> bool:
        raise NotImplementedError()
    
    @abstractmethod
    def get_image_type(self, file: UploadFile) -> str:
        raise NotImplementedError()
        
    @abstractmethod
    async def file_to_image_array(self, file: UploadFile) -> ndarray:
        raise NotImplementedError()
    
    @abstractmethod
    def draw_bounding_boxes(
        self,
        image: ndarray,
        bounding_boxes: list[ObjectLocationResponse],
        make_image_copy: bool = False,
        include_confidence_label: bool = True,
        thickness: int = 3,
        color: tuple[int, ...] = (255, 0, 255),  # red
        font_scale: int = 1
    ) -> ndarray:
        raise NotImplementedError()

    @abstractmethod
    def draw_blackout_mask(self, image_array: ndarray, resolution: ImageResolutionDto, mask: list[list[float]]) -> ndarray:
       raise NotImplementedError()