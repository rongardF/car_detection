from uuid import UUID
from datetime import datetime, timezone
from typing import Sequence, Dict, Any

from sqlalchemy import delete, update, select
from sqlalchemy.exc import IntegrityError

from common.exception import NotUniqueException, NotFoundException

# local imports
from ..model import JWTToken
from .base_repository import BaseRepository


class JWTRepository(BaseRepository[JWTToken]):
    
    def __init__(self, engine):
        super().__init__(engine, JWTToken)
    
    async def get_by_token_value(self, token_value: str) -> JWTToken:
        """
        Get entity from the database which have a 'access_token' field with
        specified value. Method call will also ensure that only single entity
        with this value exists in repository.
        
        :param token_value: User entity UUID to filter with
        :type token_value: UUID
        :return: Token entity
        :rtype: JWTToken
        """
        async with self._get_session() as session:
            query = select(self._model).where(self._model.access_token == token_value)
            scalars = await session.scalars(query)
            result = scalars.unique().all()

        if len(result) == 0:
            raise NotFoundException(key_name="access_token", entity_id=token_value, table_name=self._model.__tablename__)
        elif len(result) != 1:
            raise NotUniqueException()

        return result[0]

    async def update_by_user_id(self, user_id: UUID, values: Dict[str, Any]) -> Sequence[JWTToken]:
        """
        Update all entities from the database which have a reference (foreign key)
        to specified user ID entity.
        
        :param user_id: User entity UUID to filter with
        :type user_id: UUID
        :param values: Values/fields to be updated
        :type values: Dict[str, Any]
        :return: List of entities (rows)
        :rtype: Sequence[JWTToken]
        """
        async with self._get_session() as session:
            values = {**values, "updated_at": datetime.now(timezone.utc)}
            query = update(self._model).where(self._model.user_id == user_id).values(values).returning(self._model.id)

            try:
                scalars = await session.scalars(query)
                result = scalars.unique().all()
                await session.commit()
            except IntegrityError as error:
                self._parse_sql_error(error)

        return await self.get_multiple(result)
    
    async def delete_by_user_id(self, user_id: UUID) -> None:
        """
        Delete all entities in database that match 'user_id' field

        :param user_id: UUID of the user_id field
        :type user_id: UUID
        """
        async with self._get_session() as session:
            statements = delete(JWTToken).where(JWTToken.user_id == user_id)
            await session.execute(statements)
            try:
                await session.commit()
            except IntegrityError as error:
                self._parse_sql_error(error)