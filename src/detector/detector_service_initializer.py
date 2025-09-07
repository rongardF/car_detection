from types import TracebackType
from typing import Optional, Type

from fastapi import FastAPI
from common.initializer import State, Initializer

# local imports
from .interface import AbstractObjectCounter, AbstractAnalyzeConfigManager
from .service import ObjectCounter, ImageProcessor, AnalyzeCountConfigManager
from .detector import YoloDetector
from .database import BaseRepository, CountAnalysisConfigRepository, FrameMaskRepository, ObjectRepository


class ServiceState(State):
    vehicle_counter: AbstractObjectCounter

    analyze_count_config_manager: AbstractAnalyzeConfigManager


class DetectorServiceInitializer(Initializer):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app=app)

    async def __aenter__(self) -> ServiceState:
        state = await super().__aenter__()

        detector_used = state.config.require_config("DETECTOR_USED")
        if detector_used == "YOLOV8":
            detector = YoloDetector(confidence=0.8)
        else:
            raise ValueError("no_detector_specified")
        
        image_processor = ImageProcessor()
        vehicle_counter = ObjectCounter(object_detector=detector, image_processor=image_processor)

        # initialize repository
        analysis_config_repository = CountAnalysisConfigRepository(
            engine=self.engine_factory.create_engine("DB"),
        )

        frame_mask_repository = FrameMaskRepository(
            engine=self.engine_factory.create_engine("DB"),
        )

        object_repository = ObjectRepository(
            engine=self.engine_factory.create_engine("DB"),
        )

        analyze_count_config_manager = AnalyzeCountConfigManager(
            frame_mask_repository=frame_mask_repository,
            object_repository=object_repository,
            count_analysis_config_repository=analysis_config_repository
        )

        # self.logger.info("detector_service_initialized")

        return ServiceState(
            **state,
            vehicle_counter=vehicle_counter,
            analyze_count_config_manager=analyze_count_config_manager
        )

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        # self.logger.info("detector_service_stopped")
