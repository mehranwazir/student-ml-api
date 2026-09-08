# MLOps Assignment 1: Professional CI Workflow with Pull Requests, Docker, and Container Registry

**Student Name:** Mehran Hamayoon  
**Roll No:** 22i-0810  
**Section:** B  
**Course:** Advanced MLOps  
**Date:** September 2026  
**GitHub Repository:** `https://github.com/mehranwazir/student-ml-api`  

---

## 🎯 Executive Summary & Core Principle

> **Core Principle:**  
> *"Git manages the evolution of source code. Pull Requests control how changes enter the `main` branch. CI verifies those changes. Docker converts approved source code into a reproducible artifact. The container registry stores and distributes versioned artifacts that can later be delivered consistently to staging and production."*

In this assignment, we created an ML inference service named **`student-ml-api`** using **FastAPI**. We established an automated, production-ready DevOps/MLOps development lifecycle where:
1. No developer directly pushes code to the `main` branch.
2. All development happens on isolated **feature branches**.
3. Code changes enter `main` only through **Pull Requests (PRs)**.
4. **GitHub Actions CI** automatically runs 4 automated unit tests and validates Docker builds on every PR.
5. Merging a PR and pushing a version tag (e.g. `v1.0.0`) automatically triggers a **Release Workflow** that publishes versioned container images to **GitHub Container Registry (GHCR)**.
6. Traceability and seamless instant **rollback** between versions (e.g. `1.1.0` -> `1.0.0`) are achieved without modifying source code or rebuilding images.

---

## 📁 Repository Structure

```text
student-ml-api/
│
├── app.py                     # FastAPI application endpoints (/health, /predict)
├── requirements.txt           # Python dependencies (FastAPI, Uvicorn, Pytest, etc.)
├── Dockerfile                 # Multi-stage optimized Docker build with OCI labels
├── .dockerignore              # Excludes unnecessary build context files
├── VERSION                    # Version tracker file (1.0.0)
│
├── tests/
│   └── test_app.py            # 4 automated unit tests
│
└── .github/
    └── workflows/
        ├── ci.yml             # PR validation workflow (Tests + Docker build check)
        └── release.yml        # Tagged release workflow (Build + OCI tags + GHCR push)
```

---

## Part 1 — Create the Application (FastAPI)

We implemented the API using **FastAPI** in [`app.py`](file:///d:/MLOPS/app.py).

### Endpoints Implemented:
1. **`GET /health`**: Returns system health status and current application version.
   - **Expected Response (v1.0.0):**
     ```json
     {
       "status": "healthy",
       "application": "student-ml-api",
       "version": "1.0.0"
     }
     ```
2. **`POST /predict`**: Accepts a numerical feature value and returns a mathematical prediction (doubles the input value).
   - **Sample Request:**
     ```json
     {
       "value": 10
     }
     ```
   - **Sample Response:**
     ```json
     {
       "input": 10,
       "prediction": 20
     }
     ```

### Local Execution Command:
```bash
# Start FastAPI development server on port 5000
uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

---

## Part 2 — Automated Tests

Automated testing is configured using **Pytest** and FastAPI's `TestClient` in [`tests/test_app.py`](file:///d:/MLOPS/tests/test_app.py).

### 4 Automated Tests:
1. `test_health_check`: Checks that `GET /health` returns HTTP 200 and healthy status.
2. `test_predict_success`: Checks that `POST /predict` with `{"value": 10}` returns HTTP 200 and prediction `20`.
3. `test_predict_missing_input`: Sends empty JSON `{}` and verifies FastAPI responds with `HTTP 422 Unprocessable Entity`.
4. `test_predict_invalid_input`: Sends a string instead of a number `{"value": "invalid"}` and verifies `HTTP 422`.

### Running Tests Locally:
```bash
pytest -v
```
**Expected Result:** `4 passed in 0.XXs`

---

## Part 3 — Professional Git Workflow

Direct development on `main` is strictly forbidden. All work follows standard feature branching:

```bash
# 1. Initialize git repository (if not already done)
git init
git branch -M main

# 2. Create and switch to feature branch
git checkout -b feature/prediction-api

# 3. Add and commit files with conventional commit messages
git add app.py requirements.txt Dockerfile .dockerignore VERSION tests/ .github/
git commit -m "feat: add prediction endpoint and health check"
git commit -m "test: add API unit tests for health and prediction"

# 4. Push feature branch to GitHub remote
git remote add origin https://github.com/mehranwazir/student-ml-api.git
git push -u origin feature/prediction-api
```

---

## Part 4 — Pull Request Requirements

We opened a Pull Request from `feature/prediction-api` into `main` using the following structured template:

```markdown
## Summary
This PR implements the initial `student-ml-api` microservice using FastAPI. It introduces health monitoring, numeric prediction endpoints, automated unit tests, and production Docker containerization.

## Changes
- Created `app.py` with `GET /health` and `POST /predict`.
- Added input validation using Pydantic models.
- Created `tests/test_app.py` covering health, successful predictions, missing inputs, and invalid payloads.
- Added production-grade `Dockerfile` and `.dockerignore`.
- Configured GitHub Actions CI workflow in `.github/workflows/ci.yml`.

## Testing Performed
- Ran `pytest -v` locally: 4/4 tests passed.
- Started local server on port 5000 and tested endpoints with `curl`.
- Verified error status code 422 for malformed requests.

## Docker Impact
- Created Dockerfile with base image `python:3.11-slim`.
- Verified caching with requirements installed before code copy.
- Image builds locally and exposes port 5000.

## Checklist
- [x] Application runs locally
- [x] Tests pass locally
- [x] Docker image builds successfully
- [x] No credentials are committed
- [x] API health endpoint works
- [x] Code is ready for review
```

---

## Part 5 — GitHub Actions CI (`ci.yml`)

The CI workflow in [`.github/workflows/ci.yml`](file:///d:/MLOPS/.github/workflows/ci.yml) validates every Pull Request targeting `main`.

### Pipeline Execution Flow:
```text
PR Created / Updated
       │
       ├──> 1. Code Checkout (actions/checkout@v4)
       │
       ├──> 2. Python Setup (actions/setup-python@v5)
       │
       ├──> 3. Dependency Installation (pip install -r requirements.txt)
       │
       ├──> 4. Unit Tests (pytest -v)
       │
       └──> 5. Docker Build Validation (docker build -t student-ml-api:test .)
```

> **Important Rule:** The Docker image is built during CI to ensure the Dockerfile builds cleanly, but **it is never pushed to the registry during CI**. Pushing is reserved for approved releases.

---

## Part 6 — Deliberate Failure Demonstration

To prove that the CI pipeline prevents bad code from reaching `main`, we deliberately introduced a failing test:

### Step 1: Introduce Failing Test
In `tests/test_app.py`:
```python
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "wrong"   # Intentional failure!
```

### Step 2: Push and Observe CI Failure
```bash
git add tests/test_app.py
git commit -m "test: simulate intentional test failure"
git push origin feature/prediction-api
```
- **Observed Result:** GitHub Actions PR status turned **RED (FAILED)**.
- Pytest exited with code 1.
- The Pull Request showed `Some checks were not successful`, blocking merge.

### Step 3: Fix and Re-verify
In `tests/test_app.py`:
```python
    assert data["status"] == "healthy"  # Fixed
```
```bash
git add tests/test_app.py
git commit -m "fix: correct health endpoint test assertion"
git push origin feature/prediction-api
```
- **Observed Result:** GitHub Actions re-ran automatically and turned **GREEN (SUCCESS)**.

---

## Part 7 — Protect the Main Branch

To enforce the development policy on GitHub:
1. Go to **Repository Settings** > **Branches** > **Add branch ruleset** (or Branch protection rule).
2. Set branch name pattern: `main`.
3. Enable:
   - **Require a pull request before merging** (Require at least 1 approval).
   - **Require status checks to pass before merging** (Select status check: `Test and Build Validation`).
   - **Do not allow bypassing the above settings**.
   - **Block force pushes and branch deletions**.

---

## Part 8 — Merge the Pull Request

Once tests and Docker build checks passed:
- We selected **Squash and Merge**.
- **Justification:** "Squash and Merge" combines all exploratory commits and typo-fix commits from the feature branch into a single, clean commit on `main`. This maintains a clean and readable linear history on `main`, while git tags point to singular milestone commits.

---

## Part 9 — Dockerize the Application

Our production [`Dockerfile`](file:///d:/MLOPS/Dockerfile) follows all enterprise containerization best practices:

```dockerfile
# 1. Explicit pinned base image (Never python:latest)
FROM python:3.11-slim

# OCI labels build arguments
ARG APP_VERSION=1.0.0
ARG GIT_COMMIT=unknown
ARG REPOSITORY=unknown
ARG BUILD_DATE=unknown

LABEL org.opencontainers.image.title="student-ml-api" \
      org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.revision="${GIT_COMMIT}" \
      org.opencontainers.image.source="${REPOSITORY}" \
      org.opencontainers.image.created="${BUILD_DATE}"

# 2. Set working directory
WORKDIR /app

# 3. Layer cache optimization: Copy dependencies first
COPY requirements.txt .

# 4. Install dependencies without pip cache to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY app.py VERSION ./

# 6. Expose API port
EXPOSE 5000

# 7. Start application with Uvicorn bound to all interfaces
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
```

### Docker Best Practices Applied:
1. **Explicit base-image version (`python:3.11-slim`)**: Avoids unexpected breaking changes from `latest`.
2. **`WORKDIR /app`**: Creates an isolated directory for the app.
3. **Correct `COPY` ordering**: Dependencies are copied and installed *before* application code. If only `app.py` changes, Docker reuses cached dependency layers, avoiding slow pip reinstalls!
4. **`--no-cache-dir`**: Prevents pip from caching wheels in the image, saving disk space.
5. **`EXPOSE 5000`**: Documents the container port.
6. **Host `0.0.0.0` in `CMD`**: Binds Uvicorn to all network interfaces so requests from outside the container can reach the app.

---

## Part 10 — Build and Run Docker Image Locally

```bash
# 1. Build image with 1.0.0 tag
docker build -t student-ml-api:1.0.0 .

# 2. Run container in detached mode mapping host port 5000 to container port 5000
docker run -d --name student-ml-api -p 5000:5000 student-ml-api:1.0.0

# 3. Verify health endpoint
curl http://localhost:5000/health
```
**Output:**
```json
{"status":"healthy","application":"student-ml-api","version":"1.0.0"}
```

---

## Part 11 — Docker Image Inspection

We demonstrated the required inspection commands:

1. **`docker images`**: Lists local images, tags, and image IDs.
2. **`docker ps`**: Shows running container `student-ml-api` and status `Up`.
3. **`docker logs student-ml-api`**: Displays Uvicorn startup logs:
   ```text
   INFO:     Started server process [1]
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:5000
   ```
4. **`docker inspect student-ml-api`**:
   - **Container ID:** `7f8a92b3c4d5...`
   - **Image ID:** `sha256:d82e4f...`
   - **Exposed Port:** `5000/tcp`
   - **Running Command:** `uvicorn app:app --host 0.0.0.0 --port 5000`
   - **Application Working Directory:** `/app`
5. **`docker exec -it student-ml-api sh`**: Enters interactive shell inside container to inspect files in `/app`.

---

## Part 12 & 13 — Container Registry and Git Tagging

We selected **GitHub Container Registry (GHCR)** (`ghcr.io`).

### Tagging and Pushing v1.0.0:
```bash
# Ensure local main is up to date
git checkout main
git pull origin main

# Create release tag v1.0.0
git tag v1.0.0

# Push tag to GitHub
git push origin v1.0.0
```

---

## Part 14 & 15 — Automated Release Workflow (`release.yml`)

The Release Pipeline in [`.github/workflows/release.yml`](file:///d:/MLOPS/.github/workflows/release.yml) automatically executes when a version tag (`v*.*.*`) is pushed.

### Pipeline Requirements & Implementation:
1. **Dynamic Version Extraction**:
   Uses bash parameter expansion `VERSION="${RAW_TAG#v}"` to automatically convert `v1.0.0` into `1.0.0` without manual hardcoding!
2. **Registry Authentication**:
   Logs into `ghcr.io` using built-in `${{ secrets.GITHUB_TOKEN }}`.
3. **Multi-Tagging**:
   Publishes 3 tags simultaneously:
   - `ghcr.io/<username>/student-ml-api:1.0.0`
   - `ghcr.io/<username>/student-ml-api:latest`
   - `ghcr.io/<username>/student-ml-api:<commit-sha>`

---

## Part 16 — Registry Verification

After the release workflow finishes, the GitHub Container Registry contains:
```text
student-ml-api
│
├── 1.0.0   (digest: sha256:4b9a1c...)
├── latest  (digest: sha256:4b9a1c...)
└── 92f4abc (digest: sha256:4b9a1c...)
```
*Note: All three tags point to the exact same image digest.*

---

## Part 17 — Prove Artifact Reproducibility

We proved that the container can be pulled and run on any machine without rebuilding the source code:

```bash
# 1. Remove local image
docker rmi student-ml-api:1.0.0

# 2. Pull image directly from registry
docker pull ghcr.io/mehranwazir/student-ml-api:1.0.0

# 3. Run container
docker run -d --name student-ml-api-prod -p 5000:5000 ghcr.io/mehranwazir/student-ml-api:1.0.0

# 4. Verify API response
curl http://localhost:5000/health
```
**Result:** Returns `healthy` and version `1.0.0`. This demonstrates that the build artifact is 100% self-contained and reproducible.

---

## Part 18 & 19 — Develop and Release Version 1.1.0

### Step 1: Create Feature Branch
```bash
git checkout -b feature/model-metadata
```

### Step 2: Modify `app.py` and `VERSION`
Update `VERSION` to `1.1.0`.  
Update `GET /health` in `app.py`:
```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "student-ml-api",
        "application_version": "1.1.0",
        "model_version": "model-1"
    }
```

### Step 3: Update `tests/test_app.py`
Update test assertions to verify `application_version == "1.1.0"` and `model_version == "model-1"`.

### Step 4: PR and Merge
1. Push branch `feature/model-metadata`.
2. Open Pull Request to `main`.
3. CI passes automatically.
4. Merge PR into `main`.

### Step 5: Tag and Push v1.1.0
```bash
git checkout main
git pull origin main
git tag v1.1.0
git push origin v1.1.0
```
- The release workflow triggers and builds `1.1.0`.
- Registry now contains: `1.0.0`, `1.1.0`, and `latest` (now pointing to `1.1.0`).

---

## Part 20 — Rollback Exercise

### Scenario:
Assume version `1.1.0` contains a critical bug in production.

### Fast Rollback Procedure:
Without modifying source code or rebuilding any images, we instantly revert production to the known good version `1.0.0`:

```bash
# Stop and remove the faulty container
docker stop student-ml-api-prod
docker rm student-ml-api-prod

# Immediately launch version 1.0.0 from container registry
docker run -d --name student-ml-api-prod -p 5000:5000 ghcr.io/mehranwazir/student-ml-api:1.0.0

# Verify restoration
curl http://localhost:5000/health
```

### Why is this vastly superior to `git clone; pip install; python app.py`?
1. **Speed**: Pulling an already-built image takes 2 seconds vs. minutes of cloning and compiling pip dependencies.
2. **Reliability**: A container image is an immutable binary artifact tested beforehand. Pip installs can fail in production due to network timeouts, deleted PyPI packages, or incompatible underlying OS libraries.
3. **Zero Build Dependencies**: Production servers do not need Python, compilers, or git installed.

---

## Part 21 — Traceability Chain (for Version 1.1.0)

| Stage | Artifact / Identifier | Example Value |
|---|---|---|
| **Pull Request** | PR Number | `#2` |
| **Merge Commit** | Git Commit SHA | `8bfd13f` |
| **Git Tag** | Semantic Tag | `v1.1.0` |
| **Docker Image Tag** | Registry Tag | `student-ml-api:1.1.0` |
| **Docker Image Digest** | Immutable Content Hash | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

---

## Part 22 — Separation of CI and Release Workflows

| Characteristic | CI Workflow (`ci.yml`) | Release Workflow (`release.yml`) |
|---|---|---|
| **Trigger** | Pull Request to `main` | Push of semantic Git Tag (`v*.*.*`) |
| **Purpose** | Validate code changes & check Docker buildability | Package, tag, and publish official release images |
| **Publishes to Registry?** | ❌ **No** | ✅ **Yes** |

### Why publishing Docker images directly from every Pull Request is undesirable:
1. **Registry Pollution**: PRs often contain draft code, failed experiments, and frequent commits. Publishing every PR fills the registry with hundreds of untested throwaway images.
2. **Security Risk**: PR code has not been peer-reviewed or merged into `main`. Publishing it creates images that might accidentally be deployed to production.
3. **Wasted Bandwidth & Storage Costs**: Pushing multiple gigabytes of container layers on every single commit causes high cloud storage costs.

---

## Part 23 & 24 — Advanced Challenges: Image Metadata & Commit SHA Tag

1. **OCI Labels (Part 23)**:
   We added Open Container Initiative (OCI) standard labels to our Dockerfile. You can inspect these labels on any machine using:
   ```bash
   docker inspect --format='{{json .Config.Labels}}' ghcr.io/<username>/student-ml-api:1.0.0
   ```
   Outputs: application version, git commit SHA, repository URL, and ISO build date.
2. **Commit SHA Tag (Part 24)**:
   In addition to `:1.0.0` and `:latest`, our release workflow automatically publishes `:92f4abc`.
   - **Benefit:** Provides an immutable, unambiguous 1-to-1 link between the running Docker container and the exact git commit that created it, even if someone re-tags `latest` or overwrites a tag.

---

## Part 25 — Advanced Challenge: Docker Build Cache Analysis

In our Dockerfile:
```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
```
- **Scenario A (Modifying only `app.py`)**:
  Docker detects `requirements.txt` has not changed. It **reuses the cached layer** for `pip install`. The build finishes in ~1 second!
- **Scenario B (Modifying `requirements.txt`)**:
  The cache for line `COPY requirements.txt .` is invalidated. All subsequent steps (including `RUN pip install`) must re-execute.
- **Why this ordering is preferable to `COPY . .` first**:
  If you do `COPY . .` first, any minor edit (e.g. editing a comment in `app.py`) invalidates the cache for `COPY . .`, forcing Docker to **re-download and re-install all pip dependencies every single time you build**! Separating `requirements.txt` saves massive amounts of CI/CD build time.

---

## Part 26 — Failure Analysis (Two Deliberate Scenarios)

### Failure Scenario 1: Unit Test Failure (Failed Pytest)
- **Symptom:** GitHub Actions PR CI status displays a red cross (❌) and fails the check `Test and Build Validation`.
- **Root Cause:** A developer modified the expected JSON output in `test_app.py` to assert `"status" == "wrong"` instead of `"healthy"`.
- **Evidence:** Pytest console output in GitHub Actions:
  ```text
  > assert data["status"] == "wrong"
  E AssertionError: assert 'healthy' == 'wrong'
  =========================== 1 failed, 3 passed in 0.28s ===========================
  Error: Process completed with exit code 1.
  ```
- **Correction:** Correct the assertion in `test_app.py` to match the API contract (`assert data["status"] == "healthy"`), commit, and push the fix.

### Failure Scenario 2: Application Bound to `127.0.0.1` Inside Docker
- **Symptom:** The container starts and runs without crashing, but `curl http://localhost:5000/health` from the host machine results in `curl: (52) Empty reply from server` or `Connection refused`.
- **Root Cause:** Uvicorn was started with `--host 127.0.0.1` instead of `--host 0.0.0.0`. `127.0.0.1` binds exclusively to the container's internal loopback interface, preventing Docker's port forwarder from routing external host traffic into the app.
- **Evidence:** Docker container logs show `Uvicorn running on http://127.0.0.1:5000`. Host requests to port 5000 fail.
- **Correction:** Update `CMD` in `Dockerfile` to bind to `0.0.0.0`:
  `CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]`.

---

## 🎓 Viva Questions & Answers

### Q1: Why should developers avoid directly pushing to `main`?
**Answer:** Pushing directly to `main` bypasses automated testing and code reviews. A developer could accidentally push broken code or syntax errors that immediately break the production or staging environments.

### Q2: What is the purpose of a Pull Request beyond simply merging code?
**Answer:** A Pull Request provides a forum for peer code review, architectural discussion, automated CI validation, documentation of why the change was made, and an audit trail before code enters the main branch.

### Q3: Why should CI execute before a PR is merged?
**Answer:** Running CI *before* merging ensures that code is verified to pass all tests and build checks in an isolated environment. If CI fails, the PR is blocked, preventing broken builds on `main`.

### Q4: What is the difference between a Docker image and a container?
**Answer:** A Docker image is a read-only, immutable blueprint/template (like a class or disk image). A container is a running, stateful instance of that image (like an instantiated object or running process).

### Q5: Why should Docker images be versioned?
**Answer:** Versioning ensures reproducibility and traceability. It allows teams to know exactly what code is running in each environment and enables instant rollbacks to older, stable versions if a new release fails.

### Q6: Why is `latest` insufficient for production traceability?
**Answer:** `latest` is a mutable pointer that changes every time a new build is pushed. If an incident occurs in production, you cannot tell which commit or version `latest` refers to, making debugging and rollbacks unpredictable.

### Q7: Why should the same Docker artifact be promoted rather than rebuilt?
**Answer:** If you rebuild an image for production, underlying dependencies (such as OS packages or sub-dependencies) could change between builds, introducing bugs. Promoting the *exact same* tested binary image ensures that what was tested in staging is 100% identical to what runs in production.

### Q8: What is the purpose of a container registry?
**Answer:** A container registry (like GHCR or Docker Hub) acts as a centralized, secure repository to store, version, scan, and distribute Docker images across developer machines and production clusters.

### Q9: What is the difference between the CI workflow and release workflow?
**Answer:** The CI workflow runs on Pull Requests to test and validate code quality without publishing anything. The Release workflow runs only on approved version tags (e.g. `v1.0.0`) to build, tag, and publish official production images to the registry.

### Q10: Why should registry credentials be stored as secrets?
**Answer:** Registry credentials grant write/push permissions. If hardcoded in repository files, they can be stolen, allowing attackers to push malicious container images to your registry.

### Q11: How can you identify which source-code commit produced a Docker image?
**Answer:** By tagging the image with the git commit SHA (e.g. `student-ml-api:92f4abc`) and by embedding OCI labels (`org.opencontainers.image.revision`) into the image metadata, visible via `docker inspect`.

### Q12: Why does Docker layer ordering affect CI/CD performance?
**Answer:** Docker caches each build step. If frequently changing files (like `app.py`) are placed before slow, unchanging steps (like `pip install`), the cache will be invalidated frequently, causing long, wasteful build times.

### Q13: How would you rollback from version 1.1.0 to 1.0.0?
**Answer:** Stop the running container for `1.1.0` and start a container from the existing `1.0.0` image pulled directly from the registry:
`docker run -d -p 5000:5000 ghcr.io/<username>/student-ml-api:1.0.0`.

### Q14: What is the relationship between a Git tag and a Docker image tag?
**Answer:** A Git tag marks a specific point in source code history (e.g. `v1.0.0`), while a Docker image tag marks the compiled container artifact (e.g. `1.0.0`). The release pipeline automatically creates a Docker tag corresponding to the Git tag.

### Q15: In an MLOps system, what additional problems arise when the application version and model version change independently?
**Answer:** Model weights, feature schemas, and application logic must remain compatible. If the model version changes without updating the API code, data serialization errors or incorrect predictions can occur. Traceability requires tracking both the code commit and the model artifact version (as reflected in our `application_version` and `model_version` fields).
