import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models import ConfidenceAssessment, TelemetryEvent
from backend.schemas import ConfidenceSubmitIn, ConfidenceSubmitOut

router = APIRouter(prefix="/assessment", tags=["Assessment"])

THRESHOLD = 60.0


@router.post("/confidence", response_model=ConfidenceSubmitOut, status_code=status.HTTP_201_CREATED)
def submit_confidence(payload: ConfidenceSubmitIn, db: Session = Depends(get_db)):
    conf = payload.confidence_score
    if conf < 0.0 or conf > 100.0:
        raise HTTPException(status_code=400, detail="Confidence score must be between 0 and 100.")

    if conf < THRESHOLD:
        band = "Low"
        needs_rev = True
    elif conf < 80.0:
        band = "Moderate"
        needs_rev = False
    else:
        band = "High"
        needs_rev = False

    assessment_id = f"conf_{uuid.uuid4().hex[:12]}"
    now = datetime.utcnow()

    # Save to database
    record = ConfidenceAssessment(
        assessment_id=assessment_id,
        student_id=payload.student_id,
        topic_id=payload.topic_id,
        confidence_score=conf,
        confidence_band=band,
        needs_revision=needs_rev,
        threshold_applied=THRESHOLD,
        created_at=now
    )
    db.add(record)

    # Automatically log telemetry event
    telem = TelemetryEvent(
        event_id=f"ev_{uuid.uuid4().hex[:12]}",
        timestamp=now,
        student_id=payload.student_id,
        topic_id=payload.topic_id,
        event_type="confidence_assessment_submitted",
        confidence_score=conf,
        is_synthetic=False
    )
    db.add(telem)

    db.commit()
    db.refresh(record)

    return ConfidenceSubmitOut(
        assessment_id=record.assessment_id,
        student_id=record.student_id,
        topic_id=record.topic_id,
        confidence_score=record.confidence_score,
        confidence_band=record.confidence_band,
        needs_revision=record.needs_revision,
        threshold_applied=record.threshold_applied,
        timestamp=record.created_at
    )


@router.get("/confidence/{student_id}", response_model=List[ConfidenceSubmitOut])
def get_student_confidence(student_id: str, db: Session = Depends(get_db)):
    records = db.query(ConfidenceAssessment).filter(
        ConfidenceAssessment.student_id == student_id
    ).order_by(ConfidenceAssessment.created_at.desc()).all()

    return [
        ConfidenceSubmitOut(
            assessment_id=r.assessment_id,
            student_id=r.student_id,
            topic_id=r.topic_id,
            confidence_score=r.confidence_score,
            confidence_band=r.confidence_band,
            needs_revision=r.needs_revision,
            threshold_applied=r.threshold_applied,
            timestamp=r.created_at
        )
        for r in records
    ]
