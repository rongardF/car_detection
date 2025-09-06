from types import TracebackType
from typing import Optional, Type

from fastapi import FastAPI
from common.initializer import State, Initializer

# local imports
from .interface import AbstractVehicleCounter
from .service import VehicleCounter, ImageProcessor
from .detector import YoloDetector
from .database import CountAnalysisConfig, BaseRepository, CountAnalysisConfigRepository


class ServiceState(State):
    vehicle_counter: AbstractVehicleCounter
    analysis_config_repository: BaseRepository


class DetectorServiceInitializer(Initializer):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app=app)

    async def __aenter__(self) -> ServiceState:
        state = await super().__aenter__()

        detector_used = state.config.require_config("DETECTOR_USED")
        if detector_used == "YOLOV8":
            detector = YoloDetector(confidence=0.8)
        else:
            raise ValueError("no_detector_specifed")
        
        image_processor = ImageProcessor()
        vehicle_counter = VehicleCounter(object_detector=detector, image_processor=image_processor)

        # initialize repository
        analysis_config_repository = CountAnalysisConfigRepository(
            engine=self.engine_factory.create_engine("DB"),
        )

        # self.logger.info("detector_service_initialized")

        return ServiceState(
            **state,
            vehicle_counter=vehicle_counter,
            analysis_config_repository=analysis_config_repository
        )

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        # self.logger.info("detector_service_stopped")
