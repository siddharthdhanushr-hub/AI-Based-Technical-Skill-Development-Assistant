import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models import RevisionRecord, TelemetryEvent
from backend.schemas import RevisionOut, RevisionCompleteIn, RevisionCompleteOut
from backend.curriculum_data import REVISIONS

router = APIRouter(prefix="/revision", tags=["Revision"])


@router.get("/{topic_id}", response_model=RevisionOut)
def get_revision_content(topic_id: str):
    rev = REVISIONS.get(topic_id)
    if not rev:
        raise HTTPException(status_code=404, detail=f"No revision material found for topic '{topic_id}'")
    return rev


@router.post("/complete", response_model=RevisionCompleteOut, status_code=status.HTTP_201_CREATED)
def complete_revision(payload: RevisionCompleteIn, db: Session = Depends(get_db)):
    now = datetime.utcnow()

    # Save revision record
    rec = RevisionRecord(
        student_id=payload.student_id,
        topic_id=payload.topic_id,
        cards_reviewed_count=payload.cards_reviewed_count,
        duration_seconds=payload.duration_seconds,
        created_at=now
    )
    db.add(rec)

    # Telemetry event
    telem = TelemetryEvent(
        event_id=f"ev_{uuid.uuid4().hex[:12]}",
        timestamp=now,
        student_id=payload.student_id,
        topic_id=payload.topic_id,
        event_type="revision_completed",
        response_time_seconds=payload.duration_seconds,
        revision_status="completed",
        is_synthetic=False
    )
    db.add(telem)

    db.commit()

    return RevisionCompleteOut(
        status="recorded",
        recorded_at=now
    )
