from abc import ABC
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict, Sequence, Type, TypeVar, Generic
from uuid import UUID

from pydantic.alias_generators import to_snake
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

# local imports
from ..model import Base
from ...exception import NotFoundException

T = TypeVar("T", bound=Base)


class Repository(ABC, Generic[T]):
    """
    Abstract repository that provides ready-to-be-used get, create and update operations to
    SQLAlchemy models.

    Delete method is not provided by default because we encourage immutability, so this
    operation must be implemented by subclasses whenever applicable.
    """

    def __init__(self, engine: AsyncEngine, db_model: Type[T]):
        self._model = db_model
        self._entity_label: str = to_snake(db_model.__name__)
        self._engine: AsyncEngine = engine
        self._session_factory = async_sessionmaker(bind=self._engine, autocommit=False, autoflush=False)

    @asynccontextmanager
    async def _get_session(self, **kw: Any) -> AsyncIterator[AsyncSession]:
        session = self._session_factory(**kw)
        try:
            yield session
        finally:
            await session.close()

    async def get_all(self) -> Sequence[T]:
        """
        Fetch all entities from the database. Method uses generic type T which will be made specific
        when specific repository is implemented.

        :return: List of entities (rows)
        :rtype: Sequence[T]
        """
        async with self._get_session() as session:
            query = select(self._model)
            scalars = await session.scalars(query)
            result = scalars.unique().all()

        return result

    async def get_one(self, entity_id: UUID) -> T:
        """
        Fetch single entity from database. Method uses generic type T which will be made specific
        when specific repository is implemented.

        :param entity_id: Entity UUID to filter with
        :type entity_id: UUID
        :raises NotFoundException: If entity with specified UUID does not exist
        :return: Entity (row)
        :rtype: T
        """
        async with self._get_session() as session:
            query = select(self._model).where(self._model.id == entity_id)
            scalars = await session.scalars(query)
            result: T = scalars.unique().first()
            
            if result is None:
                raise NotFoundException(key_name="uuid", table_name=self._model.__tablename__, entity_id=entity_id)

        return result
    
    async def get_multiple(self, entity_ids: list[UUID]) -> Sequence[T]:
        """
        Fetch entities from database which are listed in the provided list of UUIDs. Method uses generic type T
        which will be made specific when specific repository is implemented.

        :param entity_ids: UUIDs of the entities to fetch
        :type entity_ids: list[UUID]
        :return: Entities with matching UUIDs
        :rtype: Sequence[T]
        """
        async with self._get_session() as session:
            statements = select(self._model).where(self._model.id.in_(entity_ids))
            scalars = await session.scalars(statements)
            result = scalars.unique().all()

        return result

    async def create(self, values: Dict[str, Any]) -> T:
        """
        Insert a new entity into database. Method uses generic type T which will be made specific
        when specific repository is implemented.

        :param values: Entity fields mapping
        :type values: Dict[str, Any]
        :return: Inserted entity
        :rtype: T
        """
        async with self._get_session() as session:
            query = insert(self._model).values(values).returning(self._model.id)

            try:
                result: UUID = await session.scalar(query)
                await session.commit()
            except IntegrityError as error:
                self._parse_sql_error(error)

        return await self.get_one(result)

    async def update(self, entity_id: UUID, values: Dict[str, Any]) -> T:
        """
        Update an entity in the database. Method uses generic type T which will be made specific
        when specific repository is implemented.

        :param entity_id: UUID of the entity to be updated
        :type entity_id: UUID
        :param values: Entity fields mapping that will be updated
        :type values: Dict[str, Any]
        :return: Updated entity
        :rtype: T
        """
        async with self._get_session() as session:
            values = {**values}
            query = update(self._model).where(self._model.id == entity_id).values(values).returning(self._model.id)

            try:
                result = await session.scalar(query)
                await session.commit()
            except IntegrityError as error:
                self._parse_sql_error(error)

        return await self.get_one(result)

    def _parse_sql_error(self, exc: IntegrityError) -> None:
        code = str(getattr(exc.orig, "pgcode", ""))
        message = str(getattr(exc.orig, "args", ""))
        self.handle_sql_error(code, message, exc)

    def handle_sql_error(self, error_code: str, error_message: str, exc: Exception) -> None:
        """
        Must handle error scenarios raised by the database, due to violation of foreign keys,
        unique keys, required column values and so on.

        Refer to https://www.postgresql.org/docs/current/errcodes-appendix.html for more
        details on codes and messages.

        :param error_code: code provided by Postgres
        :param error_message: message provided by Postgres
        :param exc: original exception raised by the ORM engine
        """
        raise NotImplementedError()
