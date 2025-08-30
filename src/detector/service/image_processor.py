import cv2
import numpy as np
from PIL import Image
from PIL.ImageFile import ImageFile
import base64
from io import BytesIO

# local imports
from ..interface import AbstractImageProcessor
from ..model import ParametersDto


class ImageProcessor(AbstractImageProcessor):

    def __init__(self):
        pass
    
    def base64_to_image(self, image_base64: str) -> ImageFile:
        image_encoded = image_base64.encode('utf-8')
        image_bytes= base64.b64decode(image_encoded)
        image_stream = BytesIO(image_bytes)
        image_stream.seek(0)

        return Image.open(image_stream)

    def image_to_base64(self, image: ImageFile) -> str:
        image_stream = BytesIO()
        image.save(image_stream, format="PNG")
        return base64.b64encode(image_stream.getvalue()).decode('utf-8')

    def draw_blackout_mask(self, image: ImageFile, parameters: ParametersDto) -> ImageFile:
        # convert to CV2 format (numpy array)
        image_rgb_array = np.array(image)
        
        # check that blackout mask does not exceed resolution boundary
        mask_array = np.array(parameters.blackout_mask)
        min = mask_array.min()
        max_width = max(mask_array[:, 0])
        max_height = max(mask_array[:, 1])
        if min < 0:
            raise ValueError("Blackout mask coordinates cannot be negative.")
        
        if max_width > parameters.resolution.width:
            raise ValueError("Blackout mask boundary (WIDTH) exceeded.")
        
        if max_height > parameters.resolution.height:
            raise ValueError("Blackout mask boundary (WIDTH) exceeded.")

        # draw blackout mask on image
        pts = mask_array.astype(np.int32).reshape((-1, 1, 2))
        blackedout_image_rgb_array = cv2.fillPoly(image_rgb_array, [pts], color=(0, 0, 0)) 

        return Image.fromarray(blackedout_image_rgb_array)