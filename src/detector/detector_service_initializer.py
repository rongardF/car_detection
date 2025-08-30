from types import TracebackType
from typing import Optional, Type

from fastapi import FastAPI
from common.initializer import State, Initializer

# local imports
from .interface.service import AbstractProcessor
from .service import Processor, ImageProcessor
from .detector import YoloDetector

class ServiceState(State):
    processor: AbstractProcessor


class DetectorServiceInitializer(Initializer):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app=app)

    async def __aenter__(self) -> ServiceState:
        state = await super().__aenter__()

        detector_used = state.config.require_config("DETECTOR_USED")
        if detector_used == "YOLOV8":
            detector = YoloDetector()
        else:
            raise TypeError("No detector specified")
        image_processor = ImageProcessor()
        processor = Processor(detector=detector, image_processor=image_processor)

        # self.logger.info("detector_service_initialized")

        return ServiceState(
            **state,
            processor=processor
        )

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        # self.logger.info("detector_service_stopped")
