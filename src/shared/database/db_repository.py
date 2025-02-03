from contextlib import asynccontextmanager
from typing import Any, Callable, Generic, Sequence, TypeVar
from psycopg import AsyncCursor, Column, sql
from exceptions import ItemBusinessError
import settings
from shared.database import db_pool
from shared.database.exceptions import PsycopgGenericException, PsycopgUniqueException
from shared.entity import Entity


T = TypeVar('T', bound=Entity)

type GenericObjectFactory[T] = Callable[[dict], T]
type GenericFieldsFactory = Callable[[list[Column]], list[str]]


class DbRepository(Generic[T]):
    def __init__(self, *,
                 table_name: str,
                 object_factory: GenericObjectFactory[T],
                 fields_factory: GenericFieldsFactory = lambda columns: [
                     col.name for col in columns],
                 is_view: bool = False,
                 identity_column: str = "id"
                 ):

        self._object_factory = object_factory
        self._fields_factory = fields_factory

        self._table_suffix = "_view" if is_view else ""
        self.table_name = table_name + self._table_suffix

        self._identity_column = identity_column

    def _row_factory(self, cursor: AsyncCursor[Any]) -> Callable[[Sequence[Any]], T]:
        fields = []

        if cursor.description != None:
            fields = self._fields_factory(cursor.description)

        def make_row(values: Sequence[Any]) -> T:
            return self._object_factory(dict(zip(fields, values)))

        return make_row

    @asynccontextmanager
    async def _cursor(self):
        async with db_pool.cursor(self._row_factory) as cursor:
            yield cursor

    async def get_all(self) -> list[T]:
        try:
            async with self._cursor() as cursor:
                await cursor.execute(
                    sql.SQL("SELECT * FROM {} ").format(
                        sql.Identifier(self.table_name))
                )

                values = await cursor.fetchall()
                return values
        except PsycopgGenericException as error:
            print(
                f"Encountered psycopg exception in get all {T} at {self.__class__}\n", error.message)

            if settings.ENVIRONMENT == "test":
                raise error

            return []

    async def get_one(self, id: str) -> T | None:
        try:
            async with self._cursor() as cursor:
                await cursor.execute(
                    sql.SQL("SELECT * FROM {} WHERE {}=%(identity)s").format(
                        sql.Identifier(self.table_name),
                        sql.Identifier(self._identity_column)),
                    {"identity": id})
                value = await cursor.fetchone()
                return value
        except PsycopgGenericException as error:
            print(
                f"Encountered psycopg exception in get one {T} at {self.__class__}\n", error.message)

            if settings.ENVIRONMENT == "test":
                raise error

    async def insert(self, payload: dict) -> T | None:
        '''
        Function will log all low level psycopg exceptions,
        and throw an ItemBusinessError on any integrity error,
        usually conflicting unique checks on rows
        '''
        try:
            async with self._cursor() as cursor:
                await cursor.execute(
                    sql.SQL("INSERT INTO {}({}) VALUES ({}) RETURNING *").format(
                        sql.Identifier(self.table_name),
                        sql.SQL(', ').join(
                            map(sql.Identifier, payload.keys())),
                        sql.SQL(', ').join(
                            map(sql.Placeholder, payload.keys()))
                    ),
                    {**payload}
                )

                inserted = await cursor.fetchone()

                return inserted
        except PsycopgUniqueException as error:
            raise ItemBusinessError(
                msg="An item with the given fields exists already") from error

        except PsycopgGenericException as error:
            print(
                f"Encountered psycopg exception in insert {T} at {self.__class__}\n", error.message)

            if settings.ENVIRONMENT == "test":
                raise error

    async def update(self, id: str, patch: dict) -> T | None:
        '''
        Function will log all low level psycopg exceptions,
        and throw an ItemBusinessError on any integrity error,
        usually conflicting unique checks on rows
        '''
        try:
            async with self._cursor() as cursor:
                await cursor.execute(
                    sql.SQL("UPDATE {} SET {} WHERE {}=%(identity)s RETURNING *").format(
                        sql.Identifier(self.table_name),
                        sql.SQL(', ').join(
                            sql.SQL("{}={}").format(
                                sql.Identifier(key),
                                sql.Placeholder(key)) for key in patch.keys()),
                        sql.Identifier(self._identity_column)
                    ),
                    {**patch, "identity": id}
                )

                patched_account = await cursor.fetchone()

                return patched_account
        except PsycopgUniqueException as error:
            print(
                f"Encountered psycopg exception in update {T} at {self.__class__}: \n", error.message)

            raise ItemBusinessError(
                msg="An item with the given fields exists already") from error
        except PsycopgGenericException as error:
            print(
                f"Encountered psycopg exception in update {T} at {self.__class__}: \n", error.message)

            if settings.ENVIRONMENT == "test":
                raise error

    async def delete(self, id: str) -> None:
        try:
            async with self._cursor() as cursor:
                await cursor.execute(
                    sql.SQL("DELETE FROM {} WHERE {}=%(identity)s").format(
                        sql.Identifier(self.table_name),
                        sql.Identifier(self._identity_column)
                    ),
                    {"identity": id}
                )
        except PsycopgGenericException as error:
            print(
                f"Encountered psycopg exception in update {T} at {self.__class__}: \n", error.message)

            if settings.ENVIRONMENT == "test":
                raise error

    async def delete_all(self) -> None:
        try:
            async with self._cursor() as cursor:
                await cursor.execute(
                    sql.SQL("DELETE FROM {}").format(
                        sql.Identifier(self.table_name),
                    )
                )
        except PsycopgGenericException as error:
            print(
                f"Encountered psycopg exception in update {T} at {self.__class__}: \n", error.message)

            if settings.ENVIRONMENT == "test":
                raise error
