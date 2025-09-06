from typing import Optional
from cv2 import fillPoly
from numpy import ndarray, uint8, frombuffer, array, int32
from cv2 import imdecode, IMREAD_COLOR, rectangle, putText, FONT_HERSHEY_SIMPLEX
from fastapi import UploadFile

# local imports
from ..interface import AbstractImageProcessor
from ..model.detector import ObjectBoundingBox, PixelCoordinate
from ..model.api.config import ImageResolution
from ..exception import MaskInvalidException, FileInvalidException


class ImageProcessor(AbstractImageProcessor):

    def __init__(self):
        pass
    
    async def file_to_image_array(self, file: UploadFile) -> ndarray:
        # Ensure its image type file
        file_extension = file.filename.lower().rsplit(".", 1)[-1]
        if f".{file_extension}" not in self.ALLOWED_EXTENSIONS:
            raise FileInvalidException()

        if file.content_type not in self.ALLOWED_MIME_TYPES:
            raise FileInvalidException()
        

        content = await file.read()

        array = frombuffer(content, uint8)
        image_array = imdecode(array, IMREAD_COLOR)

        if image_array is None:
            raise FileInvalidException("File is not a valid image.")
        
        return image_array


    def draw_bounding_boxes(
        self,
        image: ndarray,
        bounding_boxes: list[ObjectBoundingBox],
        make_image_copy: bool = False,
        include_confidence_label: bool = True,
        thickness: int = 3,
        color: tuple[int, ...] = (255, 0, 255),  # red
        font_scale: int = 1
    ) -> ndarray:
        if make_image_copy:
            image_array = image.copy()
        else:
            image_array = image

        for box in bounding_boxes:
            # Draw the bounding box on the frame
            rectangle(
                img=image_array, 
                pt1=(box.top_left.width, box.top_left.height), 
                pt2=(box.bottom_right.width, box.bottom_right.height), 
                color=color, 
                thickness=thickness
            )

            if include_confidence_label:
                text = f"{box.object_type.value}:{box.confidence}"

                putText(
                    img=image_array, 
                    text=text, 
                    org=[box.top_left.width, box.top_left.height], 
                    fontFace=FONT_HERSHEY_SIMPLEX, 
                    fontScale=font_scale, 
                    color=color, 
                    thickness=thickness
                )
        
        return image_array

    def draw_blackout_mask(self, image_array: ndarray, resolution: ImageResolution, mask: Optional[list[PixelCoordinate]]) -> ndarray:
        if mask is None:
            # no mask so nothing to do
            return image_array
        
        # check that blackout mask does not exceed resolution boundary
        pixels_list = [[pixel.width, pixel.height] for pixel in mask]
        mask_array = array(pixels_list)
        min = mask_array.min()
        max_width = max(mask_array[:, 0])
        max_height = max(mask_array[:, 1])
        if min < 0:
            raise MaskInvalidException()
        
        if max_width > resolution.width:
            raise MaskInvalidException()
        
        if max_height > resolution.height:
            raise MaskInvalidException()

        # draw blackout mask on image
        pts = mask_array.astype(int32).reshape((-1, 1, 2))
        return fillPoly(image_array, [pts], color=(0, 0, 0)) 