from types import TracebackType
from typing import Optional, Type

from cryptography.fernet import Fernet
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine
from common.initializer import State, Initializer

# local imports
from .interface import AbstractImageAnalyzer, AbstractAnalyzeImageConfigManager, AbstractBlobStorageClient, AbstractFileStorage, AbstractImageProcessor
from .service import ImageAnalyzer, ImageProcessor, AnalyzeObjectConfigManager, AuthenticationManager, BlobStorageClient, FileStorage
from .detector import YoloDetector
from .database import ObjectAnalysisConfigRepository, FrameMaskRepository, ObjectRepository, AccountRepository, APIKeyRepository, JWTRepository, FileRegisterRepository


class ServiceState(State):
    # services
    image_processor: AbstractImageProcessor
    image_analyzer: AbstractImageAnalyzer
    analyze_object_config_manager: AbstractAnalyzeImageConfigManager
    authentication_manager: AuthenticationManager
    blob_storage_client: AbstractBlobStorageClient
    file_storage: AbstractFileStorage
    # repositories
    db_engine: AsyncEngine
    account_repository: AccountRepository
    api_key_repository: APIKeyRepository
    jwt_repository: JWTRepository
    file_register_repository: FileRegisterRepository
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
        file_register_repository= FileRegisterRepository(engine=db_engine)
        analysis_config_repository = ObjectAnalysisConfigRepository(engine=db_engine)
        frame_mask_repository = FrameMaskRepository(engine=db_engine)
        object_repository = ObjectRepository(engine=db_engine)
        account_repository = AccountRepository(engine=db_engine)
        api_key_repository = APIKeyRepository(engine=db_engine)
        jwt_repository = JWTRepository(engine=db_engine)

        # initialize services/tools
        detector_used = state.config.require_config("DETECTOR_USED")
        if detector_used == "YOLOV8":
            detector = YoloDetector(confidence=0.8)
        else:
            raise ValueError("no_detector_specified")
        
        blob_storage_client = BlobStorageClient(config=state.config)
        image_processor = ImageProcessor()
        file_storage = FileStorage(
            image_processor=image_processor,
            blob_storage_client=blob_storage_client,
            file_register_repository=file_register_repository
        )
        image_analyzer = ImageAnalyzer(object_detector=detector, image_processor=image_processor)
        analyze_object_config_manager = AnalyzeObjectConfigManager(
            frame_mask_repository=frame_mask_repository,
            object_repository=object_repository,
            object_analysis_config_repository=analysis_config_repository
        )
        authentication_manager = AuthenticationManager(
            config=state.config, 
            api_key_repository=api_key_repository
        )

        # self.logger.info("detector_service_initialized")

        return ServiceState(
            **state,
            image_processor=image_processor,
            image_analyzer=image_analyzer,
            analyze_object_config_manager=analyze_object_config_manager,
            authentication_manager=authentication_manager,
            blob_storage_client=blob_storage_client,
            file_storage=file_storage,
            db_engine=db_engine,
            account_repository=account_repository,
            api_key_repository=api_key_repository,
            jwt_repository=jwt_repository,
            file_register_repository=file_register_repository,
            cipher=cipher,
        )

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        # self.logger.info("detector_service_stopped")
