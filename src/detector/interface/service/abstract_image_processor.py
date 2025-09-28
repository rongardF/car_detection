from abc import ABC, abstractmethod
from numpy import ndarray
from fastapi import UploadFile

# local imports
from ...model.dto import ObjectBoundingBoxDto
from ...model.dto import ImageResolutionDto


class AbstractImageProcessor(ABC):

    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
    ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}

    @abstractmethod
    async def file_to_image_array(self, file: UploadFile) -> ndarray:
        raise NotImplementedError()
    
    @abstractmethod
    def draw_bounding_boxes(
        self,
        image: ndarray,
        bounding_boxes: list[ObjectBoundingBoxDto],
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