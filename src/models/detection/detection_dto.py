import numpy as np
from pydantic import BaseModel, ConfigDict

from PIL import Image


class DetectionDto(BaseModel):
    model_config = ConfigDict(
        frozen=True, 
        arbitrary_types_allowed=True
    )
    
    inferred_image: Image
    boundary_boxes: np.ndarray
    count: int