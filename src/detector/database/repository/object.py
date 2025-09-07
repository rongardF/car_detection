from uuid import UUID
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

# local imports
from ..model import Object
from .base_repository import BaseRepository


class ObjectRepository(BaseRepository[Object]):
    
    def __init__(self, engine):
        super().__init__(engine, Object)

    async def get_by_count_analysis_id(self, count_analysis_config_id: UUID) -> Sequence[Object]:
        """
        Fetch all entities from the database which have a reference (foreign key)
        to specified count analysis config entity.
        
        :param count_analysis_config_id: Count analysis config entity UUID to filter with
        :type count_analysis_config_id: UUID
        :return: List of entities (rows)
        :rtype: Sequence[FrameMask]
        """
        async with self._get_session() as session:
            query = select(self._model).where(self._model.count_analysis_uuid==count_analysis_config_id)
            scalars = await session.scalars(query)
            result = scalars.unique().all()

        return result
    
    async def delete_by_count_analysis_id(self, count_analysis_config_id: UUID) -> None:
        """
        Delete all entities that match the count analysis config ID reference (foreign key)

        :param count_analysis_config_id: UUID of the count analysis config entity
        :type count_analysis_config_id: UUID
        """
        async with self._get_session() as session:
            query = select(self._model).where(self._model.count_analysis_uuid==count_analysis_config_id)
            scalars = await session.scalars(query)
            result = scalars.unique().all()
            
            try:
                for entity in result:
                    await session.delete(entity)
                await session.commit()
            except IntegrityError as error:
                self._parse_sql_error(error)