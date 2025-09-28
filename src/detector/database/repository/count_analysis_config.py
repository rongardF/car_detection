from uuid import UUID
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

# local imports
from ..model import CountAnalysisConfig
from .base_repository import BaseRepository


class CountAnalysisConfigRepository(BaseRepository[CountAnalysisConfig]):
    
    def __init__(self, engine):
        super().__init__(engine, CountAnalysisConfig)

    async def get_all_for_user_id(self, user_id: UUID) -> Sequence[CountAnalysisConfig]:
        """
        Fetch all entities from the database which have a reference (foreign key)
        to specified user ID.
        
        :param user_id: User ID to filter with
        :type user_id: UUID
        :return: List of entities (rows)
        :rtype: Sequence[CountAnalysisConfig]
        """
        async with self._get_session() as session:
            query = select(self._model).where(self._model.user_id==user_id)
            scalars = await session.scalars(query)
            result = scalars.unique().all()

        return result
    
    async def delete(self, entity_id: UUID) -> None:
        """
        Delete single entity in database

        :param entity_id: UUID of the entity to be deleted
        :type entity_id: UUID
        """
        # fetch entry to be deleted
        entry = await self.get_one(entity_id=entity_id)
        async with self._get_session() as session:
            try:
                # delete the entry
                await session.delete(entry)
                await session.commit()
            except IntegrityError as error:
                self._parse_sql_error(error)