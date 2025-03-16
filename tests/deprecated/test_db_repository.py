from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4
from pydantic import ConfigDict, Field
import pytest
from shared.psycopg import db_pool
from exceptions import ItemBusinessError
from shared.psycopg.db_repository import DbRepository
from shared.psycopg.exceptions import PsycopgGenericException
from shared.psycopg.utils import is_pg_engine_reachable
from shared.entity import Entity

pytestmark = pytest.mark.skipif(
    not is_pg_engine_reachable(), reason="PostgreSQL Engine is not reachable")


class PostgresTestData(Entity):
    model_config = ConfigDict(populate_by_name=True)

    id: UUID = Field(validation_alias="test_uuid",
                     serialization_alias="test_uuid")
    test_integer: int
    test_numeric: Decimal
    test_text: str
    test_timestamp: datetime


@pytest.fixture
def test_data_1() -> PostgresTestData:
    return PostgresTestData(
        id=uuid4(),
        test_integer=65535,
        test_numeric=Decimal('1234.5678'),
        test_text="Test Text",
        test_timestamp=datetime.now(timezone.utc)
    )


@pytest.fixture
def test_data_2() -> PostgresTestData:
    return PostgresTestData(
        id=uuid4(),
        test_integer=-128,
        test_numeric=Decimal('-0.1234'),
        test_text="Test Text 2",
        test_timestamp=datetime(1999, 1, 1, 23, 59, 59, 59, timezone.utc)
    )


@pytest.fixture(scope="module")
async def with_db_pool():
    await db_pool.db_connection_pool.open()
    yield
    await db_pool.db_connection_pool.close()


@pytest.fixture
def test_repository(with_db_pool) -> DbRepository[PostgresTestData]:
    return DbRepository(
        table_name="test_data",
        object_factory=lambda dict: PostgresTestData(**dict),
        identity_column="test_uuid"
    )


@pytest.fixture
async def empty_test_repository(test_repository) -> DbRepository[PostgresTestData]:
    await test_repository.delete_all()
    return test_repository


@pytest.fixture
async def populated_test_repository(empty_test_repository, test_data_1, test_data_2) -> DbRepository[PostgresTestData]:
    await empty_test_repository.insert(test_data_1.model_dump(by_alias=True))
    await empty_test_repository.insert(test_data_2.model_dump(by_alias=True))
    return empty_test_repository


async def test_empty_repository_read_all(empty_test_repository):
    data = await empty_test_repository.get_all()
    assert len(data) == 0


async def test_empty_repository_read(empty_test_repository):
    read = await empty_test_repository.get_one(str(uuid4()))
    assert read == None


async def test_repository_read_all(populated_test_repository, test_data_1, test_data_2):
    read = await populated_test_repository.get_all()

    assert len(read) == 2
    assert read[0] == test_data_1
    assert read[1] == test_data_2


async def test_populated_repository_read(populated_test_repository, test_data_1):
    read = await populated_test_repository.get_one(str(test_data_1.id))

    assert read != None
    assert read.id == test_data_1.id
    assert read.test_integer == test_data_1.test_integer
    assert read.test_numeric == test_data_1.test_numeric
    assert read.test_text == test_data_1.test_text
    assert read.test_timestamp == test_data_1.test_timestamp


async def test_empty_repository_insert(empty_test_repository, test_data_1):
    returned = await empty_test_repository.insert(test_data_1.model_dump(by_alias=True))

    assert returned != None
    assert returned.id == test_data_1.id
    assert returned.test_integer == test_data_1.test_integer
    assert returned.test_numeric == test_data_1.test_numeric
    assert returned.test_text == test_data_1.test_text
    assert returned.test_timestamp == test_data_1.test_timestamp


async def test_populated_repository_insert_duplicate(populated_test_repository, test_data_1):
    with pytest.raises(ItemBusinessError):
        await populated_test_repository.insert(test_data_1.model_dump(by_alias=True))


async def test_populated_repository_update(populated_test_repository, test_data_1):
    patch = {**test_data_1.model_dump(by_alias=True), "test_integer": 0}
    returned = await populated_test_repository.update(test_data_1.id, patch)

    assert returned != None
    assert returned.test_integer == 0

    returned = await populated_test_repository.get_one(test_data_1.id)

    assert returned != None
    assert returned.test_integer == 0


async def test_populated_repository_update_duplicate(populated_test_repository, test_data_1):
    patch = {**test_data_1.model_dump(by_alias=True), "test_integer": -128}

    with pytest.raises(ItemBusinessError):
        await populated_test_repository.update(test_data_1.id, patch)


async def test_populated_repository_delete(populated_test_repository, test_data_1):
    await populated_test_repository.delete(str(test_data_1.id))
    read = await populated_test_repository.get_all()

    assert len(read) == 1
    assert read[0].id != test_data_1.id


async def test_populated_repository_delete_all(populated_test_repository):
    await populated_test_repository.delete_all()
    read = await populated_test_repository.get_all()

    assert len(read) == 0


async def test_repository_invalid_arguments(empty_test_repository):
    with pytest.raises(PsycopgGenericException):
        await empty_test_repository.get_one("invalid uuid")

    with pytest.raises(PsycopgGenericException):
        await empty_test_repository.insert({})

    with pytest.raises(PsycopgGenericException):
        await empty_test_repository.update("invalid uuid", {})

    with pytest.raises(PsycopgGenericException):
        await empty_test_repository.delete("invalid uuid")
