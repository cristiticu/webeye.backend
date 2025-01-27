
from contextlib import asynccontextmanager
from typing import Any, Callable, Sequence, TypeVar
from psycopg import AsyncCursor, Error, IntegrityError
from psycopg_pool import AsyncConnectionPool
from settings import POSTGRES_ADDRESS, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB_NAME
from shared.database.exceptions import PsycopgGenericException, PsycopgIntegrityException
from shared.entity import Entity

T = TypeVar('T', bound=Entity)

connection_string = f"postgresql://{POSTGRES_USER}:{
    POSTGRES_PASSWORD}@{POSTGRES_ADDRESS}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"


db_connection_pool = AsyncConnectionPool(connection_string, open=False)


@asynccontextmanager
async def cursor(row_factory: Callable[[AsyncCursor[Any]], Callable[[Sequence[Any]], T]]):
    async with db_connection_pool.connection() as connection:
        async with connection.cursor(row_factory=row_factory) as cursor:
            try:
                yield cursor
            except IntegrityError as error:
                if error.sqlstate == "23505":
                    raise PsycopgIntegrityException(error) from error
                else:
                    raise PsycopgGenericException(error) from error
            except Error as error:
                raise PsycopgGenericException(error) from error
