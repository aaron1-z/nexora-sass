import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Nexora Intelligence Engine API v2"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "operational"

# Add more tests for:
# - Ingestion logic
# - Reasoner output
# - Auth validation
