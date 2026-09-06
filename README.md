# Student ML API (MLOps Assignment 1)

Welcome to the **Student ML API** repository! This project demonstrates an end-to-end MLOps pipeline covering API development with FastAPI, automated unit testing with Pytest, containerization with Docker, and CI/CD automation with GitHub Actions and GitHub Container Registry (GHCR).

---

## 📁 Repository Structure

```text
student-ml-api/
│
├── app.py                     # FastAPI application source code
├── requirements.txt           # Python dependencies (FastAPI, Pytest, etc.)
├── Dockerfile                 # Docker configuration for containerizing the API
├── .dockerignore              # Files excluded from Docker builds
├── VERSION                    # Current application version (e.g., 1.0.0)
│
├── tests/
│   └── test_app.py            # Automated unit tests using Pytest
│
└── .github/
    └── workflows/
        ├── ci.yml             # Pull Request CI workflow (Test + Docker build check)
        └── release.yml        # Release CI/CD workflow (Publish versioned image to GHCR)
```

---

## 🚀 Quick Start (Local Setup)

### 1. Create and Activate Virtual Environment

```bash
# Create a virtual environment
python -m venv .venv

# Activate on Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Or activate on Linux/macOS
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the API Locally

```bash
uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

Open your browser at:
- Interactive API Docs: `http://localhost:5000/docs`
- Health Endpoint: `http://localhost:5000/health`

### 4. Run Automated Tests

```bash
pytest -v
```

---

## 🐳 Docker Usage

### 1. Build the Docker Image Locally

```bash
docker build -t student-ml-api:1.0.0 .
```

### 2. Run the Docker Container

```bash
docker run -d --name student-ml-api -p 5000:5000 student-ml-api:1.0.0
```

### 3. Test the Containerized API

```bash
# Test health check
curl http://localhost:5000/health

# Test prediction
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d "{\"value\": 10}"
```

### 4. Stop and Remove the Container

```bash
docker stop student-ml-api
docker rm student-ml-api
```

---

## 🔄 CI/CD Workflows Overview

1. **Pull Request CI (`ci.yml`)**:
   - Runs automatically when a PR is created targeting `main`.
   - Runs `pytest` and verifies that `docker build` succeeds.
   - **Does not** publish any image.

2. **Automated Release Workflow (`release.yml`)**:
   - Triggers only when a Git tag like `v1.0.0` is pushed.
   - Automatically derives version `1.0.0` from `v1.0.0`.
   - Attaches OCI metadata labels and Git commit SHA.
   - Publishes to GitHub Container Registry (`ghcr.io`).
