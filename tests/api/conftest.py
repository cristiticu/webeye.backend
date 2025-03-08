from fastapi.testclient import TestClient
import pytest
from src.main import app


@pytest.fixture
def test_client():
    return TestClient(app)
