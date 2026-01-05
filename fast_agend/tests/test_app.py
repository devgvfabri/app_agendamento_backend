from fastapi.testclient import TestClient
from fast_agend.app import app


def test_root_deve_retornar_ola_mundo():
    client  = TestClient(app)

    response = client.get('/')

    assert response.json() == {'message': 'Olá mundo'}


