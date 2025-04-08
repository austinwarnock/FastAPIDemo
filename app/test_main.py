from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_get_weather():
    response = client.get("/39.7456,-97.0892")
    assert response.status_code == 200
    data = response.json()
    assert "properties" in data

def test_get_weather_invalid_location():
    response = client.get("/invalid_location")
    assert response.status_code == 500
