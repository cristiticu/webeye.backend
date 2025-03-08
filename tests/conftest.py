import pytest
import context
import settings
from tests.mocks.monitored_webpage.persistence import MockedMonitoredWebpagePersistence
from tests.mocks.user_account.persistence import MockedUserAccountPersistence


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(settings, "ENVIRONMENT", "test")


@pytest.fixture(autouse=True)
def mock_all_persistences(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        context.ApplicationContext.instance.monitored_webpages, "_webpages", MockedMonitoredWebpagePersistence())
    monkeypatch.setattr(context.ApplicationContext.instance.user_accounts,
                        "_users", MockedUserAccountPersistence())
