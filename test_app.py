# test_app.py
import json
import pytest
from app import app


@pytest.fixture
def client():
    app.testing = True
    return app.test_client()


def test_search_valid_query(client):
    response = client.get("/search?q=test")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert all("title" in item and "url" in item for item in data)


def test_search_empty_query(client):
    response = client.get("/search")
    assert response.status_code == 400
