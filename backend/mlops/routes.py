"""
MLOps FastAPI Route Controller
Endpoints for 21st-Century Skill Assessment, ML Inference, Tracker Sync, and MLOps Insights.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from backend.core import database
from backend.user import auth
from backend.user.models import Student
from .service import mlops_service
from .constants import (
    CENTURY_21_SKILLS,
    ROLE_REQUIREMENTS,
    ROLE_CLASSES,
    EXCLUDED_LEGACY_SKILLS,
    PHASE1_METRICS,
    PHASE2_GOVERNANCE
)

router = APIRouter()

class EvaluateSkillsRequest(BaseModel):
    skills: Dict[str, float] = Field(..., description="Mapping of skill id to proficiency rating (0.0 to 6.0)")
    target_role: Optional[str] = Field("Software Developer", description="Target technical career role")
    threshold: Optional[float] = Field(0.50, description="Pass probability decision threshold (default 0.50)")

class SyncTrackerRequest(BaseModel):
    role_name: Optional[str] = None
    role: Optional[str] = None
    skills: Optional[List[str]] = None
    gap_skills: Optional[List[str]] = None

@router.get("/config")
def get_mlops_configuration():
    """
    Returns the 21st-Century Skills taxonomy, role definitions, and legacy pruning justifications.
    """
    return {
        "skills": CENTURY_21_SKILLS,
        "century_21_skills": CENTURY_21_SKILLS,
        "roles": ROLE_CLASSES,
        "role_requirements": ROLE_REQUIREMENTS,
        "excluded_legacy_skills": EXCLUDED_LEGACY_SKILLS,
        "default_threshold": 0.50,
        "rating_scale": {
            "min": 0,
            "max": 6,
            "levels": [
                {"score": 0, "label": "No Exposure", "badge": "Novice"},
                {"score": 1, "label": "Conceptual Awareness", "badge": "Beginner"},
                {"score": 2, "label": "Basic Implementation", "badge": "Foundational"},
                {"score": 3, "label": "Working Competency", "badge": "Intermediate"},
                {"score": 4, "label": "Independent Problem Solver", "badge": "Proficient"},
                {"score": 5, "label": "Advanced & Scalable", "badge": "Advanced"},
                {"score": 6, "label": "Production Mastery", "badge": "Expert"}
            ]
        }
    }

@router.post("/evaluate")
def evaluate_student_skills(
    payload: EvaluateSkillsRequest,
    current_user: Student = Depends(auth.get_current_user)
):
    """
    Executes the trained Phase 2 Random Forest champion model + ensemble voting.
    Determines whether student is ready for the direct verification quiz or should prepare in the tracker.
    Traced using MLflow Observability (Experiment 1).
    """
    try:
        from backend.mlops.tracing import trace_competency_prediction
        try:
            return trace_competency_prediction(payload.skills, user_id=str(current_user.student_id))
        except Exception as trace_err:
            print(f"Tracing fallback note: {trace_err}")
            return mlops_service.predict_student_assessment(
                user_scores=payload.skills,
                target_role=payload.target_role,
                threshold=payload.threshold or 0.50
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(e)}"
        )

@router.post("/sync-tracker")
def sync_gap_skills_to_tracker(
    payload: SyncTrackerRequest,
    current_user: Student = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """
    Syncs identified gap skills to the user's Skill Tracker so they can study Skill Briefs,
    Flashcards, Hints, and Projects before attempting the verification quiz.
    """
    target_skills = payload.skills or payload.gap_skills or []
    target_role = payload.role_name or payload.role or "Software Developer"

    if not target_skills:
        raise HTTPException(status_code=400, detail="No skills provided to sync")

    result = mlops_service.sync_skills_to_tracker(
        student_id=current_user.student_id,
        skills_to_sync=target_skills,
        role_name=target_role,
        db=db
    )
    return result

@router.get("/verification-quiz")
def get_verification_quiz(
    current_user: Student = Depends(auth.get_current_user)
):
    """
    Provides the 10-question cross-verification quiz directly assessing 21st-century tech skills.
    """
    questions = mlops_service.get_21st_century_verification_quiz()
    return {
        "title": "21st-Century Technical Assessment Cross-Verification",
        "description": "Cross-verifying your self-reported proficiency with 10 industry screening questions.",
        "total_questions": len(questions),
        "questions": questions
    }

@router.get("/insights")
def get_mlops_insights():
    """
    Returns full Phase 1 and Phase 2 MLOps reports, evaluation benchmarks, and governance lineage.
    """
    return {
        "phase1": PHASE1_METRICS,
        "phase1_metrics": PHASE1_METRICS,
        "phase2": PHASE2_GOVERNANCE,
        "phase2_governance": PHASE2_GOVERNANCE
    }
