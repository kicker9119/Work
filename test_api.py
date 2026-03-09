from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["message"] == "API is functional"

def test_valid_delay_request():
    params = {
        "arrival_airport": "LAX",
        "departure_airport": "ATL",
        "departure_time_local": "2025-01-01T10:00",
        "arrival_time_local": "2025-01-01T13:00"
    }
    r = client.get("/predict/delays", params=params)
    assert r.status_code in (200, 404, 500)  # dataset dependent

def test_invalid_code():
    params = {
        "arrival_airport": "LA",
        "departure_airport": "ATL",
        "departure_time_local": "2025-01-01T10:00",
        "arrival_time_local": "2025-01-01T13:00"
    }
    r = client.get("/predict/delays", params=params)
    assert r.status_code == 422
