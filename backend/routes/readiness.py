from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.core.database import get_db
from backend.models import ConfidenceAssessment, QuizAttempt, RevisionRecord
from backend.schemas import TopicReadinessOut, ProgressSummaryOut
from backend.curriculum_data import TOPICS

router = APIRouter(prefix="/readiness", tags=["Readiness & Progress"])


def _calculate_topic_readiness(student_id: str, topic_id: str, db: Session) -> TopicReadinessOut:
    # 1. Latest confidence rating
    latest_conf = db.query(ConfidenceAssessment).filter(
        ConfidenceAssessment.student_id == student_id,
        ConfidenceAssessment.topic_id == topic_id
    ).order_by(ConfidenceAssessment.created_at.desc()).first()

    # 2. Quiz attempts
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.student_id == student_id,
        QuizAttempt.topic_id == topic_id
    ).order_by(QuizAttempt.created_at.desc()).all()

    # 3. Revision status
    rev_count = db.query(RevisionRecord).filter(
        RevisionRecord.student_id == student_id,
        RevisionRecord.topic_id == topic_id
    ).count()

    conf_score = latest_conf.confidence_score if latest_conf else None
    conf_band = latest_conf.confidence_band if latest_conf else "Unrated"

    attempts_count = len(attempts)
    latest_score = attempts[0].score_percentage if attempts else None
    best_score = max([a.score_percentage for a in attempts]) if attempts else None
    has_revised = rev_count > 0

    # Calculate readiness category strictly based on evidence
    if attempts_count == 0:
        readiness_status = "Not Yet Assessed"
        rec = "Take a topic quiz or review concept flashcards to demonstrate mastery."
    else:
        latest = attempts[0]
        readiness_status = latest.readiness_status
        rec = latest.recommended_action

    return TopicReadinessOut(
        student_id=student_id,
        topic_id=topic_id,
        confidence_score=conf_score,
        confidence_band=conf_band,
        latest_quiz_score=latest_score,
        best_quiz_score=best_score,
        attempts_count=attempts_count,
        revision_completed=has_revised,
        readiness_status=readiness_status,
        recommended_next_action=rec
    )


@router.get("/progress/{student_id}", response_model=ProgressSummaryOut)
def get_overall_progress(student_id: str, db: Session = Depends(get_db)):
    breakdown = []
    assessed_count = 0
    weak_count = 0

    for topic in TOPICS:
        t_id = topic["topic_id"]
        t_readiness = _calculate_topic_readiness(student_id, t_id, db)
        breakdown.append(t_readiness)

        if t_readiness.confidence_score is not None:
            assessed_count += 1
            if t_readiness.confidence_score < 60.0:
                weak_count += 1

    # Total quizzes taken by student
    total_quizzes = db.query(QuizAttempt).filter(QuizAttempt.student_id == student_id).count()
    avg_score_res = db.query(func.avg(QuizAttempt.score_percentage)).filter(QuizAttempt.student_id == student_id).scalar()
    avg_score = round(float(avg_score_res), 1) if avg_score_res is not None else 0.0

    return ProgressSummaryOut(
        student_id=student_id,
        topics_assessed=assessed_count,
        weak_topics_count=weak_count,
        quizzes_taken=total_quizzes,
        average_quiz_score=avg_score,
        topic_readiness_breakdown=breakdown
    )


@router.get("/{student_id}/{topic_id}", response_model=TopicReadinessOut)
def get_topic_readiness(student_id: str, topic_id: str, db: Session = Depends(get_db)):
    return _calculate_topic_readiness(student_id, topic_id, db)
