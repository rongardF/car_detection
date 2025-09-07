from uuid import UUID

from sqlalchemy.exc import IntegrityError

# local imports
from ..model import CountAnalysisConfig
from .base_repository import BaseRepository


class CountAnalysisConfigRepository(BaseRepository[CountAnalysisConfig]):
    
    def __init__(self, engine):
        super().__init__(engine, CountAnalysisConfig)

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