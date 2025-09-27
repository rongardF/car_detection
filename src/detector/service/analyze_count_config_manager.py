from uuid import UUID

from common.exception.repository_exception import NotFoundException

# local imports
from ..model.enum import ObjectEnum
from ..model.api import CountAnalysisConfigRequest, CountAnalysisConfigResponse, ImageResolution, PixelCoordinate
from ..exception.api import ConfigureNotFoundException
from ..interface import AbstractAnalyzeConfigManager
from ..database import FrameMaskRepository, ObjectRepository, CountAnalysisConfigRepository


class AnalyzeCountConfigManager(AbstractAnalyzeConfigManager[CountAnalysisConfigRequest, CountAnalysisConfigResponse]):

    def __init__(
        self,
        frame_mask_repository: FrameMaskRepository,
        object_repository: ObjectRepository,
        count_analysis_config_repository: CountAnalysisConfigRepository
    ):
        self._frame_mask_repository = frame_mask_repository
        self._object_repository = object_repository
        self._count_analysis_config_repository = count_analysis_config_repository

    def _validate_is_users_config(self, user_id: UUID, config: CountAnalysisConfigResponse):
        pass

    async def add_config(self, user_id: UUID, request: CountAnalysisConfigRequest) -> CountAnalysisConfigResponse:
        count_analysis_config = await self._count_analysis_config_repository.create(
            values={
                "user_id": user_id,
                "image_resolution_width": request.image_resolution.width,
                "image_resolution_height": request.image_resolution.height,
                "confidence": request.confidence,
            }
        )
        for object in request.objects:
            await self._object_repository.create(
                values={
                    "value": object,
                    "count_analysis_config": count_analysis_config.id
                }
            )

        for pixel_coordinate in request.image_mask:
            await self._frame_mask_repository.create(
                values={
                    "pixel_width": pixel_coordinate.width,
                    "pixel_height": pixel_coordinate.height,
                    "count_analysis_config": count_analysis_config.id
                }
            )
        
        return CountAnalysisConfigResponse(
            id=count_analysis_config.id,
            **request.model_dump()
        )
    
    async def get_config(self, user_id: UUID, config_id: UUID) -> CountAnalysisConfigResponse:
        frame_mask_points = await self._frame_mask_repository.get_by_count_analysis_id(
            count_analysis_config_id=config_id
        )
        objects = await self._object_repository.get_by_count_analysis_id(
            count_analysis_config_id=config_id
        )
        try:
            count_analysis_config = await self._count_analysis_config_repository.get_one(
                entity_id=config_id
            )
        except NotFoundException as err:
            raise ConfigureNotFoundException(f"entity_{err.entity_id}_not_found_in_{err.table_name}")
        
        self._validate_is_users_config(user_id, count_analysis_config)

        return CountAnalysisConfigResponse(
            id=count_analysis_config.id,
            user_id=count_analysis_config.user_id,
            confidence=count_analysis_config.confidence,
            image_resolution=ImageResolution(
                width=count_analysis_config.image_resolution_width,
                height=count_analysis_config.image_resolution_height
            ),
            image_mask=[
                PixelCoordinate(width=mask.pixel_width,height=mask.pixel_height) for mask in frame_mask_points
            ],
            objects=[
                ObjectEnum(object.value) for object in objects
            ]
        )
    
    async def get_all_configs(self, user_id: UUID) -> list[CountAnalysisConfigResponse]:
        count_analysis_configs = await self._count_analysis_config_repository.get_all_for_user_id(
            user_id=user_id
        )

        configurations: list[CountAnalysisConfigResponse] = []
        for config in count_analysis_configs:
            frame_mask_points = await self._frame_mask_repository.get_by_count_analysis_id(
                count_analysis_config_id=config.id
            )
            objects = await self._object_repository.get_by_count_analysis_id(
                count_analysis_config_id=config.id
            )

            configurations.append(
                CountAnalysisConfigResponse(
                    id=config.id,
                    user_id=user_id,
                    confidence=config.confidence,
                    image_resolution=ImageResolution(
                        width=config.image_resolution_width,
                        height=config.image_resolution_height
                    ),
                    image_mask=[
                        PixelCoordinate(width=mask.pixel_width,height=mask.pixel_height) for mask in frame_mask_points
                    ],
                    objects=[
                        ObjectEnum(object.value) for object in objects
                    ]
                )
            )
        
        return configurations
    
    async def update_config(self, user_id: UUID, config_id: UUID, request: CountAnalysisConfigRequest) -> CountAnalysisConfigResponse:
        try:
            count_analysis_config = await self._count_analysis_config_repository.get_one(entity_id=config_id)

            self._validate_is_users_config(user_id, count_analysis_config)

            # delete old entities and add new
            await self._frame_mask_repository.delete_by_count_analysis_id(count_analysis_config_id=config_id)
            for pixel_coordinate in request.image_mask:
                await self._frame_mask_repository.create(
                    values={
                        "pixel_width": pixel_coordinate.width,
                        "pixel_height": pixel_coordinate.height,
                        "count_analysis_config": config_id
                    }
                )

            await self._object_repository.delete_by_count_analysis_id(count_analysis_config_id=config_id)      
            for object in request.objects:
                await self._object_repository.create(
                    values={
                        "value": object,
                        "count_analysis_config": config_id
                    }
                )

            updated_count_analysis_config = await self._count_analysis_config_repository.update(
                entity_id=config_id,
                values={
                    "image_resolution_width": request.image_resolution.width,
                    "image_resolution_height": request.image_resolution.height
                }
            )
        except NotFoundException as err:
            raise ConfigureNotFoundException(f"entity_{err.entity_id}_not_found_in_{err.table_name}")

        return CountAnalysisConfigResponse(
            id=updated_count_analysis_config.id,
            **request.model_dump()
        )
    
    async def delete_config(self, user_id: UUID, config_id: UUID) -> None:
        try:
            await self._count_analysis_config_repository.delete(entity_id=config_id)
        except NotFoundException as err:
            raise ConfigureNotFoundException(f"entity_{err.entity_id}_not_found_in_{err.table_name}")