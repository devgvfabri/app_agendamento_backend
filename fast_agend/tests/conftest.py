from fastapi.testclient import TestClient
from fast_agend.app import app
from sqlalchemy import create_engine
from fast_agend.models import table_registry
import pytest

@pytest.fixture
def client():
    return TestClient(app)

def session():
    engine = create_engine
    table_registry.metadata.create_all(engine)
