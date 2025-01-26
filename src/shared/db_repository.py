from typing import Any, Callable, Generic, Sequence, TypeVar
from psycopg import AsyncCursor, Column
from shared.entity import Entity


T = TypeVar('T', bound=Entity)

type GenericObjectFactory[T] = Callable[[dict], T]
type GenericFieldsFactory = Callable[[list[Column]], list[str]]


class DbRepository(Generic[T]):
    def __init__(self, *, object_factory: GenericObjectFactory[T], fields_factory: GenericFieldsFactory = lambda columns: [col.name for col in columns]):
        self._object_factory = object_factory
        self._fields_factory = fields_factory

    def _row_factory(self, cursor: AsyncCursor[Any]) -> Callable[[Sequence[Any]], T]:
        fields = []

        if cursor.description != None:
            fields = self._fields_factory(cursor.description)

        def make_row(values: Sequence[Any]) -> T:
            return self._object_factory(dict(zip(fields, values)))

        return make_row
