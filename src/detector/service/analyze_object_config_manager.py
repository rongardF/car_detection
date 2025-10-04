from uuid import UUID

from common.exception.repository_exception import NotFoundException

# local imports
from ..model.enum import ObjectEnum
from ..model.api import ObjectAnalysisConfigResponse, ObjectAnalysisConfigRequest, ImageResolution, PixelCoordinate
from ..exception.api import ConfigureNotFoundException, AccountUnAuthorizedException
from ..interface import AbstractAnalyzeImageConfigManager
from ..database import FrameMaskRepository, ObjectRepository, CountAnalysisConfigRepository, CountAnalysisConfig


class AnalyzeObjectConfigManager(AbstractAnalyzeImageConfigManager[ObjectAnalysisConfigRequest, ObjectAnalysisConfigResponse]):

    def __init__(
        self,
        frame_mask_repository: FrameMaskRepository,
        object_repository: ObjectRepository,
        count_analysis_config_repository: CountAnalysisConfigRepository
    ):
        self._frame_mask_repository = frame_mask_repository
        self._object_repository = object_repository
        self._count_analysis_config_repository = count_analysis_config_repository

    def _validate_is_users_config(self, user_id: UUID, config: CountAnalysisConfig):
        if config.user_id != user_id:
            raise AccountUnAuthorizedException()

    async def add_config(self, user_id: UUID, request: ObjectAnalysisConfigRequest) -> ObjectAnalysisConfigResponse:
        count_analysis_config = await self._count_analysis_config_repository.create(
            values={
                "user_id": user_id,
                "image_resolution_width": request.image_resolution.width,
                "image_resolution_height": request.image_resolution.height,
                "confidence": request.confidence,
            }
        )

        objects: list[ObjectEnum] = []
        for request_object in request.objects:
            object = await self._object_repository.create(
                values={
                    "value": request_object,
                    "count_analysis_config": count_analysis_config.id
                }
            )
            objects.append(ObjectEnum(object.value))

        image_mask: list[PixelCoordinate] = []
        if request.image_mask:
            for pixel_coordinate in request.image_mask:
                coordinate = await self._frame_mask_repository.create(
                    values={
                        "pixel_width": pixel_coordinate.width,
                        "pixel_height": pixel_coordinate.height,
                        "count_analysis_config": count_analysis_config.id
                    }
                )
                image_mask.append(
                    PixelCoordinate(
                        width=coordinate.pixel_width,
                        height=coordinate.pixel_height
                    )
                )
        
        return ObjectAnalysisConfigResponse(
            id=count_analysis_config.id,
            confidence=count_analysis_config.confidence,
            image_resolution=ImageResolution(
                width=count_analysis_config.image_resolution_width,
                height=count_analysis_config.image_resolution_height
            ),
            image_mask=image_mask if image_mask else None,
            objects=objects
        )
    
    async def get_config(self, user_id: UUID, config_id: UUID) -> ObjectAnalysisConfigResponse:
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

        return ObjectAnalysisConfigResponse(
            id=count_analysis_config.id,
            user_id=count_analysis_config.user_id,
            confidence=count_analysis_config.confidence,
            image_resolution=ImageResolution(
                width=count_analysis_config.image_resolution_width,
                height=count_analysis_config.image_resolution_height
            ),
            image_mask=[
                PixelCoordinate(width=mask.pixel_width,height=mask.pixel_height) for mask in v
            ] if frame_mask_points else None,
            objects=[
                ObjectEnum(object.value) for object in objects
            ]
        )
    
    async def get_all_configs(self, user_id: UUID) -> list[ObjectAnalysisConfigResponse]:
        count_analysis_configs = await self._count_analysis_config_repository.get_all_for_user_id(
            user_id=user_id
        )

        configurations: list[ObjectAnalysisConfigResponse] = []
        for config in count_analysis_configs:
            frame_mask_points = await self._frame_mask_repository.get_by_count_analysis_id(
                count_analysis_config_id=config.id
            )
            objects = await self._object_repository.get_by_count_analysis_id(
                count_analysis_config_id=config.id
            )

            configurations.append(
                ObjectAnalysisConfigResponse(
                    id=config.id,
                    user_id=user_id,
                    confidence=config.confidence,
                    image_resolution=ImageResolution(
                        width=config.image_resolution_width,
                        height=config.image_resolution_height
                    ),
                    image_mask=[
                        PixelCoordinate(width=mask.pixel_width,height=mask.pixel_height) for mask in frame_mask_points
                    ] if frame_mask_points else None,
                    objects=[
                        ObjectEnum(object.value) for object in objects
                    ]
                )
            )
        
        return configurations
    
    async def update_config(self, user_id: UUID, config_id: UUID, request: ObjectAnalysisConfigRequest) -> ObjectAnalysisConfigResponse:
        try:
            count_analysis_config = await self._count_analysis_config_repository.get_one(entity_id=config_id)

            self._validate_is_users_config(user_id, count_analysis_config)

            # delete old entities and add new
            await self._frame_mask_repository.delete_by_count_analysis_id(count_analysis_config_id=config_id)
            image_mask: list[PixelCoordinate] = []
            if request.image_mask:
                for pixel_coordinate in request.image_mask:
                    coordinate = await self._frame_mask_repository.create(
                        values={
                            "pixel_width": pixel_coordinate.width,
                            "pixel_height": pixel_coordinate.height,
                            "count_analysis_config": config_id
                        }
                    )
                    image_mask.append(
                        PixelCoordinate(
                            width=coordinate.pixel_width,
                            height=coordinate.pixel_height
                        )
                    )

            await self._object_repository.delete_by_count_analysis_id(count_analysis_config_id=config_id)      
            objects: list[ObjectEnum] = []
            for request_object in request.objects:
                object = await self._object_repository.create(
                    values={
                        "value": request_object,
                        "count_analysis_config": config_id
                    }
                )
                objects.append(ObjectEnum(object.value))

            updated_count_analysis_config = await self._count_analysis_config_repository.update(
                entity_id=config_id,
                values={
                    "image_resolution_width": request.image_resolution.width,
                    "image_resolution_height": request.image_resolution.height,
                    "confidence": request.confidence,
                }
            )
        except NotFoundException as err:
            raise ConfigureNotFoundException(f"entity_{err.entity_id}_not_found_in_{err.table_name}")

        return ObjectAnalysisConfigResponse(
            id=updated_count_analysis_config.id,
            confidence=updated_count_analysis_config.confidence,
            image_resolution=ImageResolution(
                width=updated_count_analysis_config.image_resolution_width,
                height=updated_count_analysis_config.image_resolution_height
            ),
            image_mask=image_mask if image_mask else None,
            objects=objects
        )
    
    async def delete_config(self, user_id: UUID, config_id: UUID) -> None:
        try:
            count_analysis_config = await self._count_analysis_config_repository.get_one(entity_id=config_id)
            self._validate_is_users_config(user_id, count_analysis_config)
            await self._count_analysis_config_repository.delete(entity_id=config_id)
        except NotFoundException as err:
            raise ConfigureNotFoundException(f"entity_{err.entity_id}_not_found_in_{err.table_name}")