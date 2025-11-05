from uuid import UUID
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

# local imports
from ..model import File
from .base_repository import BaseRepository


class FileRegisterRepository(BaseRepository[File]):
    
    def __init__(self, engine):
        super().__init__(engine, File)

    async def get_by_account_id(self, account_id: UUID) -> Sequence[File]:
        """
        Fetch all entities from the database which have a reference (foreign key)
        to specified account ID.
        
        :param account_id: Account ID
        :type account_id: UUID
        :return: List of entities (rows)
        :rtype: Sequence[File]
        """
        async with self._get_session() as session:
            query = select(self._model).where(self._model.account_id==account_id)
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