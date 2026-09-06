# Step 1: Use an explicit, lightweight official Python base image (not latest)
FROM python:3.11-slim

# Build arguments for OCI metadata labels (Part 23)
ARG APP_VERSION=1.0.0
ARG GIT_COMMIT=unknown
ARG REPOSITORY=unknown
ARG BUILD_DATE=unknown

# Standard OCI labels for image traceability
LABEL org.opencontainers.image.title="student-ml-api" \
      org.opencontainers.image.description="Student ML API inference service" \
      org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.revision="${GIT_COMMIT}" \
      org.opencontainers.image.source="${REPOSITORY}" \
      org.opencontainers.image.created="${BUILD_DATE}"

# Step 2: Set working directory inside container
WORKDIR /app

# Step 3: Copy only requirements.txt first to take advantage of Docker layer caching
COPY requirements.txt .

# Step 4: Install dependencies without storing pip cache to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy application code and version file
COPY app.py VERSION ./

# Step 6: Expose port 5000 for FastAPI
EXPOSE 5000

# Step 7: Run FastAPI application using Uvicorn server bound to 0.0.0.0
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
