# Multi-stage production Dockerfile for AI-Based Technical Skill Development Assistant
FROM python:3.11-slim as runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8005

# Install system dependencies (curl for healthchecks, tesseract for OCR)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create a non-privileged user and group for container security
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -s /bin/bash -m appuser

# Install pinned dependencies first to leverage Docker layer caching
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and pre-trained model artifacts
COPY backend/ /app/backend/

# Create uploads directory and assign permissions to non-root user
RUN mkdir -p /app/uploads && chown -R appuser:appgroup /app

USER appuser

EXPOSE 8005

# Container liveness & readiness healthcheck probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8005/health || exit 1

# Launch production ASGI server via Uvicorn
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8005", "--workers", "1"]
