from uuid import UUID
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

# local imports
from ..model import FrameMask
from .base_repository import BaseRepository


class FrameMaskRepository(BaseRepository[FrameMask]):
    
    def __init__(self, engine):
        super().__init__(engine, FrameMask)

    async def get_by_object_analysis_id(self, object_analysis_config_id: UUID) -> Sequence[FrameMask]:
        """
        Fetch all entities from the database which have a reference (foreign key)
        to specified object analysis config entity.
        
        :param object_analysis_config_id: Object analysis config entity UUID to filter with
        :type object_analysis_config_id: UUID
        :return: List of entities (rows)
        :rtype: Sequence[FrameMask]
        """
        async with self._get_session() as session:
            query = select(self._model).where(self._model.object_analysis_config==object_analysis_config_id)
            scalars = await session.scalars(query)
            result = scalars.unique().all()

        return result
    
    async def delete_by_object_analysis_id(self, object_analysis_config_id: UUID) -> None:
        """
        Delete all entities that match the object analysis config ID reference (foreign key)

        :param object_analysis_config_id: UUID of the object analysis config entity
        :type object_analysis_config_id: UUID
        """
        async with self._get_session() as session:
            query = select(self._model).where(self._model.object_analysis_config==object_analysis_config_id)
            scalars = await session.scalars(query)
            result = scalars.unique().all()
            
            try:
                for entity in result:
                    await session.delete(entity)
                await session.commit()
            except IntegrityError as error:
                self._parse_sql_error(error)