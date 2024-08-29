from typing import Dict, Any, Tuple

from src.interfaces import (
    AbstractVehicleDetector,
    AbstractProcessor,
    AbstractImageProcessor
)
from src.models import ParametersDto


class Processor(AbstractProcessor):

    def __init__(
        self, 
        image_processor: AbstractImageProcessor,
        detector: AbstractVehicleDetector,
    ):
        self._vechicle_detector = detector
        self._image_processor = image_processor

    def process(
        self,
        image_base64: str,
        parameters_dict: Dict[str, Any]
    ) -> Tuple[int, str]:
        image = self._image_processor.base64_to_image(image_base64)
        parameters = ParametersDto(**parameters_dict)

        blacked_out_image = self._image_processor.draw_blackout_mask(image, parameters)

        detection_data = self._vechicle_detector.detect_and_count(blacked_out_image)

        result_image_base64 = self._image_processor.image_to_base64(detection_data.inferred_image)  # TODO: add an option in parameters which specifies if reply shoudl include processed image or not

        return (detection_data.count, result_image_base64)