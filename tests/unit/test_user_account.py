from datetime import datetime, timezone
from uuid import uuid4
import pytest
from context import ApplicationContext
from user_account.exceptions import UserAccountNotFound
from user_account.model import CreateUserAccount, UserAccount

application_context = ApplicationContext()


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


async def test_user_service_get_all():
    data = await application_context.user_accounts.get_all()

    assert len(data) == 0


async def test_user_service_get_one(mock_user_1):
    user = await application_context.user_accounts.create(CreateUserAccount(email="test2@email.com",
                                                                            password="1234",
                                                                            first_name="Second",
                                                                            last_name="Last 2",))
    read = await application_context.user_accounts.get(str(user.id))

    assert read != None


async def test_user_service_get_invalid():
    with pytest.raises(UserAccountNotFound):
        await application_context.user_accounts.get("invalid id")
