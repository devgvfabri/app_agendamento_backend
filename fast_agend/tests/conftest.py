from fastapi.testclient import TestClient
from fast_agend.app import app
import pytest

@pytest.fixture
def client():
    return TestClient(app)