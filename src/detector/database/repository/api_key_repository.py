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
    
    async def get_by_account_id(self, account_id: UUID) -> Sequence[APIKey]:
        """
        Fetch all entities from the database which have a reference (foreign key)
        to specified account ID entity.
        
        :param account_id: Account entity UUID to filter with
        :type account_id: UUID
        :return: List of entities (rows)
        :rtype: Sequence[APIKey]
        """
        async with self._get_session() as session:
            query = select(self._model).where(self._model.account_id==account_id)
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
    
    async def delete_with_account_id(self, entity_id: UUID, account_id: UUID) -> None:
        """
        Delete single entity in database that matches provided account ID value.

        :param entity_id: UUID of the entity to be deleted
        :type entity_id: UUID
        :param account_id: Account UUID of the entity that must match
        :type account_id: UUID
        """
        # fetch entry to be deleted
        entry = await self.get_one(entity_id=entity_id)
        if entry.account_id != account_id:
            raise NotFoundException(key_name="account_id", entity_id=account_id, table_name=self._model.__tablename__)
        
        async with self._get_session() as session:
            try:
                # delete the entry
                await session.delete(entry)
                await session.commit()
            except IntegrityError as error:
                self._parse_sql_error(error)
    
    async def delete_by_account_id(self, account_id: UUID) -> None:
        """
        Delete all entities in database that match 'account_id' field

        :param account_id: UUID of the account_id field
        :type account_id: UUID
        """
        async with self._get_session() as session:
            statements = delete(APIKey).where(APIKey.account_id == account_id)
            await session.execute(statements)
            try:
                await session.commit()
            except IntegrityError as error:
                self._parse_sql_error(error)