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
        guid=uuid4(),
        email="test@email.com",
        password="1234",
        first_name="First",
        last_name="Last",
        added_at=datetime.now(timezone.utc)
    )


@pytest.fixture
def mock_user_2():
    return UserAccount(
        guid=uuid4(),
        email="test2@email.com",
        password="1234",
        first_name="Second",
        last_name="Last 2",
        added_at=datetime(1999, 1, 1, 1, 1, 1, 1, timezone.utc)
    )


def test_user_service_get_all():
    data = application_context.user_accounts.get_all()

    assert len(data) == 0


def test_user_service_get_one(mock_user_1):
    user = application_context.user_accounts.create(CreateUserAccount(email="test2@email.com",
                                                                            password="1234",
                                                                            first_name="Second",
                                                                            last_name="Last 2",))
    read = application_context.user_accounts.get(str(user.guid))

    assert read != None


def test_user_service_get_invalid():
    with pytest.raises(UserAccountNotFound):
        application_context.user_accounts.get("invalid id")
