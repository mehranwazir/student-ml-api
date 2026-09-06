import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ensure root folder is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

# Create a test client for FastAPI
client = TestClient(app)

# Test 1: Verify health endpoint returns status 200 and healthy
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["application"] == "student-ml-api"
    assert "version" in data

# Test 2: Verify successful prediction with valid numeric input
def test_predict_success():
    payload = {"value": 10}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["input"] == 10
    assert data["prediction"] == 20

# Test 3: Verify error handling when input payload is missing
def test_predict_missing_input():
    payload = {}
    response = client.post("/predict", json=payload)
    # FastAPI returns 422 Unprocessable Entity when required field is missing
    assert response.status_code == 422

# Test 4: Verify error handling when input type is invalid (string instead of number)
def test_predict_invalid_input():
    payload = {"value": "invalid_number"}
    response = client.post("/predict", json=payload)
    # FastAPI returns 422 Unprocessable Entity when validation fails
    assert response.status_code == 422
