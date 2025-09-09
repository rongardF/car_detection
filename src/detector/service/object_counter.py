from fastapi import UploadFile

# local imports
from ..interface.detector import AbstractObjectDetector
from ..interface import AbstractImageProcessor, AbstractObjectCounter
from ..model.enum import ObjectEnum
from ..model.api import ObjectCountResponse, CountAnalysisConfigResponse


class ObjectCounter(AbstractObjectCounter):

    def __init__(self, object_detector: AbstractObjectDetector, image_processor: AbstractImageProcessor) -> None:
        self._object_detector = object_detector
        self._image_processor = image_processor

    async def count(self, file: UploadFile, count_analysis: CountAnalysisConfigResponse) -> ObjectCountResponse:
        image_array = await self._image_processor.file_to_image_array(file=file)
        masked_image_array = self._image_processor.draw_blackout_mask(image_array=image_array, resolution=count_analysis.image_resolution, mask=count_analysis.image_mask)
        detected_objects = self._object_detector.count(image=masked_image_array, objects=count_analysis.objects, confidence=count_analysis.confidence)

        objects_count = {
            object.value: detected_objects.get(object, 0) for object in count_analysis.objects
        }

        return ObjectCountResponse(objects=objects_count)
        
