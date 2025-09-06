from fastapi import UploadFile

# local imports
from ..interface.detector import AbstractObjectDetector
from ..interface import AbstractImageProcessor, AbstractVehicleCounter
from ..model.enum import ObjectEnum
from ..model.api import VehicleCountResponse, CountAnalysisConfigResponse


class VehicleCounter(AbstractVehicleCounter):

    OBJECTS_MAPPING: dict[ObjectEnum] = [ObjectEnum.BICYCLE, ObjectEnum.CAR, ObjectEnum.BUS, ObjectEnum.TRUCK, ObjectEnum.MOTORBIKE]

    def __init__(self, object_detector: AbstractObjectDetector, image_processor: AbstractImageProcessor) -> None:
        self._object_detector = object_detector
        self._image_processor = image_processor

    async def count(self, file: UploadFile, count_analysis: CountAnalysisConfigResponse) -> VehicleCountResponse:
        image_array = await self._image_processor.file_to_image_array(file=file)
        masked_image_array = self._image_processor.draw_blackout_mask(image_array=image_array, resolution=count_analysis.image_resolution, mask=count_analysis.image_mask)
        detected_objects = self._object_detector.count(image=masked_image_array, objects=count_analysis.objects)

        if ObjectEnum.VEHICLE in count_analysis.objects:
            # if vehicles object specified then we count for all vehicle types
            # no matter what else is specified
            vehicles = [
                ObjectEnum.CAR, 
                ObjectEnum.MOTORBIKE, 
                ObjectEnum.BICYCLE, 
                ObjectEnum.BUS, 
                ObjectEnum.TRUCK
            ]
        else:
            # we only count the vehicle types specified
            vehicles = count_analysis.objects

        vehicles_count = {
            vehicle: detected_objects.get(vehicle, 0) for vehicle in vehicles
        }

        return VehicleCountResponse(
            vehicles_total=sum(vehicles_count.values()),
            motorbikes=vehicles_count.get(ObjectEnum.MOTORBIKE, 0),
            trucks=vehicles_count.get(ObjectEnum.TRUCK, 0),
            buses=vehicles_count.get(ObjectEnum.BUS, 0),
            bicycles=vehicles_count.get(ObjectEnum.BICYCLE, 0),
            cars=vehicles_count.get(ObjectEnum.CAR, 0),
        )
        
