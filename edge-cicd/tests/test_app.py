"""
Test Suite for Edge Sensor Node API
=====================================
These tests run automatically in the CI/CD pipeline (GitHub Actions)
every time code is pushed to the repository.
"""

import pytest
import json
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── Home Endpoint Tests ───────────────────────────────────────────────────────

class TestHomeEndpoint:
    def test_home_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_home_returns_json(self, client):
        response = client.get("/")
        data = json.loads(response.data)
        assert "service" in data
        assert "version" in data
        assert "status" in data

    def test_home_service_name(self, client):
        response = client.get("/")
        data = json.loads(response.data)
        assert data["service"] == "Edge Sensor Node"

    def test_home_status_running(self, client):
        response = client.get("/")
        data = json.loads(response.data)
        assert data["status"] == "running"


# ── Health Check Tests ────────────────────────────────────────────────────────

class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_status_healthy(self, client):
        response = client.get("/health")
        data = json.loads(response.data)
        assert data["status"] == "healthy"


# ── Sensor Endpoint Tests ─────────────────────────────────────────────────────

class TestSensorsEndpoint:
    def test_sensors_returns_200(self, client):
        response = client.get("/sensors")
        assert response.status_code == 200

    def test_sensors_has_device_id(self, client):
        response = client.get("/sensors")
        data = json.loads(response.data)
        assert "device_id" in data

    def test_sensors_has_readings(self, client):
        response = client.get("/sensors")
        data = json.loads(response.data)
        assert "readings" in data
        readings = data["readings"]
        assert "temperature_c" in readings
        assert "humidity_percent" in readings
        assert "cpu_load_percent" in readings

    def test_temperature_in_valid_range(self, client):
        for _ in range(10):  # Run multiple times to check randomness
            response = client.get("/sensors/temperature")
            data = json.loads(response.data)
            assert 20.0 <= data["value"] <= 45.0

    def test_humidity_in_valid_range(self, client):
        for _ in range(10):
            response = client.get("/sensors/humidity")
            data = json.loads(response.data)
            assert 30.0 <= data["value"] <= 90.0

    def test_cpu_in_valid_range(self, client):
        for _ in range(10):
            response = client.get("/sensors/cpu")
            data = json.loads(response.data)
            assert 5.0 <= data["value"] <= 95.0


# ── Alert Endpoint Tests ──────────────────────────────────────────────────────

class TestAlertsEndpoint:
    def test_alerts_returns_200(self, client):
        response = client.get("/alerts")
        assert response.status_code == 200

    def test_alerts_has_count(self, client):
        response = client.get("/alerts")
        data = json.loads(response.data)
        assert "alert_count" in data
        assert isinstance(data["alert_count"], int)

    def test_alerts_has_list(self, client):
        response = client.get("/alerts")
        data = json.loads(response.data)
        assert "alerts" in data
        assert isinstance(data["alerts"], list)


# ── Negative Tests ────────────────────────────────────────────────────────────

class TestNegativeCases:
    def test_invalid_route_returns_404(self, client):
        response = client.get("/invalid-route")
        assert response.status_code == 404
