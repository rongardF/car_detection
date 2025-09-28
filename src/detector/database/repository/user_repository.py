from uuid import UUID
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

# local imports
from ..model import User
from .base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    
    def __init__(self, engine):
        super().__init__(engine, User)

    async def get_by_email(self, email: str) -> Sequence[User]:
        """
        Fetch entities from database which have a matching 'email' field

        :param email: Email field value
        :type email: str
        :return: Entities with matching UUIDs
        :rtype: Sequence[User]
        """
        async with self._get_session() as session:
            statements = select(self._model).where(self._model.email==email)
            scalars = await session.scalars(statements)
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