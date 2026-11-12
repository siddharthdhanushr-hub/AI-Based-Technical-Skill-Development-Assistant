import os
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import pandas as pd
from backend.core.database import get_db
from backend.models import TelemetryEvent
from backend.schemas import TelemetryEventIn

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])


@router.post("/event", status_code=status.HTTP_201_CREATED)
def record_telemetry_event(payload: TelemetryEventIn, db: Session = Depends(get_db)):
    event = TelemetryEvent(
        event_id=payload.event_id,
        timestamp=payload.timestamp,
        student_id=payload.student_id,
        topic_id=payload.topic_id,
        event_type=payload.event_type,
        attempt_id=payload.attempt_id,
        question_id=payload.question_id,
        confidence_score=payload.confidence_score,
        selected_option=payload.selected_option,
        is_correct=payload.is_correct,
        response_time_seconds=payload.response_time_seconds,
        quiz_score=payload.quiz_score,
        revision_status=payload.revision_status,
        readiness_status=payload.readiness_status,
        is_synthetic=payload.is_synthetic
    )
    db.add(event)
    db.commit()
    return {"status": "success", "event_id": payload.event_id}


@router.get("/events/{student_id}", response_model=List[Dict[str, Any]])
def get_student_telemetry(student_id: str, limit: int = 50, db: Session = Depends(get_db)):
    records = db.query(TelemetryEvent).filter(
        TelemetryEvent.student_id == student_id
    ).order_by(TelemetryEvent.timestamp.desc()).limit(limit).all()

    return [
        {
            "event_id": r.event_id,
            "timestamp": r.timestamp.isoformat() + "Z",
            "student_id": r.student_id,
            "topic_id": r.topic_id,
            "event_type": r.event_type,
            "confidence_score": r.confidence_score,
            "quiz_score": r.quiz_score,
            "readiness_status": r.readiness_status,
            "is_synthetic": r.is_synthetic
        }
        for r in records
    ]


@router.post("/export/csv")
def export_telemetry_to_csv(output_path: str = "data/raw/live_telemetry_export.csv", db: Session = Depends(get_db)):
    records = db.query(TelemetryEvent).all()
    if not records:
        return {"status": "empty", "message": "No telemetry records found to export."}

    rows = []
    for r in records:
        rows.append({
            "event_id": r.event_id,
            "timestamp": r.timestamp.isoformat() + "Z",
            "student_id": r.student_id,
            "topic_id": r.topic_id,
            "event_type": r.event_type,
            "attempt_id": r.attempt_id,
            "question_id": r.question_id,
            "confidence_score": r.confidence_score,
            "selected_option": r.selected_option,
            "is_correct": r.is_correct,
            "response_time_seconds": r.response_time_seconds,
            "quiz_score": r.quiz_score,
            "revision_status": r.revision_status,
            "readiness_status": r.readiness_status,
            "is_synthetic": r.is_synthetic
        })

    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    return {"status": "success", "rows_exported": len(df), "path": output_path}
