from fastapi import UploadFile

# local imports
from ..interface.detector import AbstractObjectDetector
from ..interface import AbstractImageProcessor, AbstractImageAnalyzer
from ..model.api import ObjectCountResponse, ObjectLocationResponse, ObjectAnalysisConfigResponse


class ImageAnalyzer(AbstractImageAnalyzer):

    def __init__(self, object_detector: AbstractObjectDetector, image_processor: AbstractImageProcessor) -> None:
        self._object_detector = object_detector
        self._image_processor = image_processor

    async def count_objects(self, file: UploadFile, object_analysis_config: ObjectAnalysisConfigResponse) -> list[ObjectCountResponse]:
        image_array = await self._image_processor.file_to_image_array(file=file)
        masked_image_array = self._image_processor.draw_blackout_mask(image_array=image_array, resolution=object_analysis_config.image_resolution, mask=object_analysis_config.image_mask)
        counted_objects = self._object_detector.count(image=masked_image_array, objects=object_analysis_config.objects, confidence=object_analysis_config.confidence)

        objects_count = [
            ObjectCountResponse(
                object_type=object_enum,
                object_count=counted_objects.get(object_enum, 0))
                for object_enum in object_analysis_config.objects
        ]

        return objects_count
    
    async def locate_objects(self, file: UploadFile, object_analysis_config: ObjectAnalysisConfigResponse) -> list[ObjectLocationResponse]:
        image_array = await self._image_processor.file_to_image_array(file=file)
        masked_image_array = self._image_processor.draw_blackout_mask(image_array=image_array, resolution=object_analysis_config.image_resolution, mask=object_analysis_config.image_mask)
        grouped_located_objects = self._object_detector.detect(image=masked_image_array, objects=object_analysis_config.objects, confidence=object_analysis_config.confidence)
        
        located_objects = []
        for objects_group in grouped_located_objects.values():
            for object_location in objects_group:
                located_objects.append(
                    ObjectLocationResponse.from_bounding_box(object_location)
                )

        return located_objects
        
