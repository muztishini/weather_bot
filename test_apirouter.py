from fastapi.testclient import TestClient
from main import app
from typing import List

client = TestClient(app)


def test_get_logs():
    response = client.get("/logs")
    assert response.status_code == 200
    assert isinstance(response.json(), List)


def test_get_user_logs():
    response = client.get("/logs/5010667130")
    assert response.status_code == 200
    assert isinstance(response.json(), List)
