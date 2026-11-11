import os
import sys

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.database import engine, Base
import backend.models

# Auto-create SQLite database tables on startup
Base.metadata.create_all(bind=engine)

# Import API routers
from backend.routes.curriculum import router as curriculum_router
from backend.routes.assessment import router as assessment_router
from backend.routes.revision import router as revision_router
from backend.routes.quiz import router as quiz_router
from backend.routes.readiness import router as readiness_router
from backend.routes.telemetry import router as telemetry_router
from backend.routes.models import router as models_router

app = FastAPI(
    title="AI-Based Technical Skill Development Assistant API",
    description="Backend services, telemetry event capture, assessment scoring, and baseline ML inference.",
    version="1.0.0"
)

# Enable CORS for local Vite development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(curriculum_router, prefix="/api")
app.include_router(assessment_router, prefix="/api")
app.include_router(revision_router, prefix="/api")
app.include_router(quiz_router, prefix="/api")
app.include_router(readiness_router, prefix="/api")
app.include_router(telemetry_router, prefix="/api")
app.include_router(models_router, prefix="/api")


@app.get("/")
def root():
    return {
        "project": "AI-Based Technical Skill Development Assistant",
        "phase": "Phase 1: Development and Reproducibility",
        "status": "online",
        "docs_url": "/docs"
    }


@app.get("/health")
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "database": "sqlite",
        "ml_inference": "active",
        "service": "AI-Based Technical Skill Development Assistant"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
