from fastapi.testclient import TestClient
from main import app
from typing import List

client = TestClient(app)


def test_read_logs():
    response = client.get("/logs")
    assert response.status_code == 200
    assert isinstance(response.json(), List)
