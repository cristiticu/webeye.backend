from datetime import datetime, timezone
from uuid import uuid4
import pytest
from exceptions import ItemBusinessError
import shared.database.db_repository
from user_account.exceptions import UserAccountNotFound
from user_account.model import UserAccount
from user_account.persistence import UserAccountPersistence
from user_account.service import UserAccountService


@pytest.fixture
def mock_user_1():
    return UserAccount(
        id=uuid4(),
        email="test@email.com",
        password="1234",
        first_name="First",
        last_name="Last",
        added_at=datetime.now(timezone.utc)
    )


@pytest.fixture
def mock_user_2():
    return UserAccount(
        id=uuid4(),
        email="test2@email.com",
        password="1234",
        first_name="Second",
        last_name="Last 2",
        added_at=datetime(1999, 1, 1, 1, 1, 1, 1, timezone.utc)
    )


@pytest.fixture
def mock_user_persistence(monkeypatch, mock_user_1, mock_user_2):
    async def mock_get_all(self):
        mock_users: list[UserAccount] = [mock_user_1, mock_user_2]

        return mock_users

    async def mock_get_one(self, id: str):
        mock_users: list[UserAccount] = await self.get_all()
        mock_user: list[UserAccount] = [
            user for user in mock_users if str(user.id) == id]

        return mock_user[0] if len(mock_user) > 0 else None

    async def mock_insert(self, payload: dict):
        mock_users: list[UserAccount] = await self.get_all()

        for user in mock_users:
            if user.email == payload["email"]:
                raise ItemBusinessError()

        return UserAccount(**{**payload, "id": uuid4()})

    monkeypatch.setattr(
        shared.database.db_repository.DbRepository, "get_all", mock_get_all)
    monkeypatch.setattr(
        shared.database.db_repository.DbRepository, "get_one", mock_get_one)
    monkeypatch.setattr(
        shared.database.db_repository.DbRepository, "insert", mock_insert)

    return UserAccountPersistence()


@pytest.fixture
def service(mock_user_persistence):
    return UserAccountService(mock_user_persistence)


async def test_user_service_get_all(service):
    data = await service.get_all()

    assert len(data) == 2


async def test_user_service_get_one(service, mock_user_1):
    read = await service.get(str(mock_user_1.id))

    assert read != None


async def test_user_service_get_invalid(service):
    with pytest.raises(UserAccountNotFound):
        await service.get("invalid id")
