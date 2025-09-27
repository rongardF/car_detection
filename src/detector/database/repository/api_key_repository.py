from uuid import UUID
from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError

from common.exception import NotFoundException

# local imports
from ..model import APIKey
from .base_repository import BaseRepository


class APIKeyRepository(BaseRepository[APIKey]):
    
    def __init__(self, engine):
        super().__init__(engine, APIKey)
    
    async def get_by_user_id(self, user_id: UUID) -> Sequence[APIKey]:
        """
        Fetch all entities from the database which have a reference (foreign key)
        to specified user ID entity.
        
        :param user_id: User entity UUID to filter with
        :type user_id: UUID
        :return: List of entities (rows)
        :rtype: Sequence[APIKey]
        """
        async with self._get_session() as session:
            query = select(self._model).where(self._model.user_id==user_id)
            scalars = await session.scalars(query)
            result = scalars.unique().all()

        return result
    
    async def get_by_hashed_key(self, hashed_key: str) -> APIKey:
        """
        Fetch entity which has a matching 'hashed_key' value.
        
        :param hashed_key: Encrypted key value to match with
        :type hashed_key: bytes
        :return: Matching API key entity
        :rtype: APIKey
        """
        async with self._get_session() as session:
            query = select(self._model).where(self._model.hashed_key == hashed_key)
            scalars = await session.scalars(query)
            result = scalars.unique().first()

        if result is None:
            raise NotFoundException(key_name="hashed_key", entity_id=hashed_key, table_name=self._model.__tablename__)

        return result
    
    async def delete_with_user_id(self, entity_id: UUID, user_id: UUID) -> None:
        """
        Delete single entity in database that matches provided user ID value.

        :param entity_id: UUID of the entity to be deleted
        :type entity_id: UUID
        :param user_id: User UUID of the entity that must match
        :type user_id: UUID
        """
        # fetch entry to be deleted
        entry = await self.get_one(entity_id=entity_id)
        if entry.user_id != user_id:
            raise NotFoundException(key_name="user_id", entity_id=user_id, table_name=self._model.__tablename__)
        
        async with self._get_session() as session:
            try:
                # delete the entry
                await session.delete(entry)
                await session.commit()
            except IntegrityError as error:
                self._parse_sql_error(error)
    
    async def delete_by_user_id(self, user_id: UUID) -> None:
        """
        Delete all entities in database that match 'user_id' field

        :param user_id: UUID of the user_id field
        :type user_id: UUID
        """
        async with self._get_session() as session:
            statements = delete(APIKey).where(APIKey.user_id == user_id)
            await session.execute(statements)
            try:
                await session.commit()
            except IntegrityError as error:
                self._parse_sql_error(error)