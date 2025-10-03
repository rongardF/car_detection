from types import TracebackType
from typing import Optional, Type

from cryptography.fernet import Fernet
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine
from common.initializer import State, Initializer

# local imports
from .interface import AbstractImageAnalyzer, AbstractAnalyzeImageConfigManager
from .service import ImageAnalyzer, ImageProcessor, AnalyzeObjectConfigManager, AuthenticationManager
from .detector import YoloDetector
from .database import CountAnalysisConfigRepository, FrameMaskRepository, ObjectRepository, UserRepository, APIKeyRepository, JWTRepository


class ServiceState(State):
    # services
    image_analyzer: AbstractImageAnalyzer
    analyze_object_config_manager: AbstractAnalyzeImageConfigManager
    authentication_manager: AuthenticationManager
    # repositories
    db_engine: AsyncEngine
    user_repository: UserRepository
    api_key_repository: APIKeyRepository
    jwt_repository: JWTRepository
    # utilities
    cipher: Fernet
    

class DetectorServiceInitializer(Initializer):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app=app)

    async def __aenter__(self) -> ServiceState:
        state = await super().__aenter__()

        # DB engine
        db_engine = self.engine_factory.create_engine("DB")

        # initialize utilities
        api_key_encryption = state.config.require_config("API_KEY_ENCRYPTION")
        cipher = Fernet(api_key_encryption.encode())

        # initialize repositories
        analysis_config_repository = CountAnalysisConfigRepository(engine=db_engine)
        frame_mask_repository = FrameMaskRepository(engine=db_engine)
        object_repository = ObjectRepository(engine=db_engine)
        user_repository = UserRepository(engine=db_engine)
        api_key_repository = APIKeyRepository(engine=db_engine)
        jwt_repository = JWTRepository(engine=db_engine)

        # initialize services/tools
        detector_used = state.config.require_config("DETECTOR_USED")
        if detector_used == "YOLOV8":
            detector = YoloDetector(confidence=0.8)
        else:
            raise ValueError("no_detector_specified")
        
        image_processor = ImageProcessor()
        image_analyzer = ImageAnalyzer(object_detector=detector, image_processor=image_processor)
        analyze_object_config_manager = AnalyzeObjectConfigManager(
            frame_mask_repository=frame_mask_repository,
            object_repository=object_repository,
            count_analysis_config_repository=analysis_config_repository
        )
        authentication_manager = AuthenticationManager(
            config=state.config, 
            api_key_repository=api_key_repository
        )

        # self.logger.info("detector_service_initialized")

        return ServiceState(
            **state,
            image_analyzer=image_analyzer,
            analyze_object_config_manager=analyze_object_config_manager,
            authentication_manager=authentication_manager,
            db_engine=db_engine,
            user_repository=user_repository,
            api_key_repository=api_key_repository,
            jwt_repository=jwt_repository,
            cipher=cipher,
        )

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        # self.logger.info("detector_service_stopped")
