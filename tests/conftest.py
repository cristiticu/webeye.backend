import pytest

import settings


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setattr(settings, "ENVIRONMENT", "test")
