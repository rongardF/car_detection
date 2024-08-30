from typing import Dict, Any, Tuple

from src.interfaces import (
    AbstractVehicleDetector,
    AbstractProcessor,
    AbstractImageProcessor
)
from src.models import (
    DetectionRequestDto,
    ProcessRequestDto, 
    ProcessResultDto
)


class Processor(AbstractProcessor):

    def __init__(
        self, 
        image_processor: AbstractImageProcessor,
        detector: AbstractVehicleDetector,
    ):
        self._vechicle_detector = detector
        self._image_processor = image_processor

    def process(self, process_request: ProcessRequestDto) -> ProcessResultDto:
        image = self._image_processor.base64_to_image(
            image_base64=process_request.image_base64
        )

        blacked_out_image = self._image_processor.draw_blackout_mask(
            image=image, 
            parameters=process_request.parameters
        )

        detection_request = DetectionRequestDto(
            process_request=process_request,
            image=blacked_out_image
        )

        detection_result = self._vechicle_detector.detect_and_count(
            detection_request=detection_request
        )

        if process_request.parameters.return_inferred_image:
            result_image_base64 = (
                self._image_processor.image_to_base64(
                    image=detection_result.inferred_image
                )
            )
        else:
            result_image_base64 = None

        return ProcessResultDto(
            process_request=process_request,
            detection_result=detection_result, 
            inferred_image_base64=result_image_base64,
        )