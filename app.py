from fastapi import FastAPI
from pydantic import BaseModel
import os

# Create the FastAPI app instance
app = FastAPI(title="student-ml-api")

# Function to read version from VERSION file
def get_version() -> str:
    version_file = os.path.join(os.path.dirname(__file__), "VERSION")
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            return f.read().strip()
    return "1.0.0"

# Request model for prediction endpoint
class PredictionRequest(BaseModel):
    value: float

# Health Check Endpoint (Version 1.1.0)
@app.get("/health")
def health_check():
    # Returns status, application name, application version, and model version
    return {
        "status": "healthy",
        "application": "student-ml-api",
        "application_version": get_version(),
        "model_version": "model-1"
    }

# Prediction Endpoint
@app.post("/predict")
def predict(request: PredictionRequest):
    # Simple mathematical prediction: doubles the input value
    prediction_result = request.value * 2
    return {
        "input": request.value,
        "prediction": prediction_result
    }
