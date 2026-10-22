from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.core.database import Base


class ConfidenceAssessment(Base):
    __tablename__ = "confidence_assessments"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(String(64), unique=True, index=True)
    student_id = Column(String(64), index=True, nullable=False)
    topic_id = Column(String(64), index=True, nullable=False)
    confidence_score = Column(Float, nullable=False)
    confidence_band = Column(String(32), nullable=False)
    needs_revision = Column(Boolean, default=False)
    threshold_applied = Column(Float, default=60.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class RevisionRecord(Base):
    __tablename__ = "revision_records"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(64), index=True, nullable=False)
    topic_id = Column(String(64), index=True, nullable=False)
    cards_reviewed_count = Column(Integer, default=0)
    duration_seconds = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(String(64), unique=True, index=True, nullable=False)
    student_id = Column(String(64), index=True, nullable=False)
    topic_id = Column(String(64), index=True, nullable=False)
    score_percentage = Column(Float, nullable=False)
    total_questions = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    readiness_status = Column(String(32), nullable=False)
    recommended_action = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    responses = relationship("QuestionResponse", back_populates="attempt", cascade="all, delete-orphan")


class QuestionResponse(Base):
    __tablename__ = "question_responses"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(String(64), ForeignKey("quiz_attempts.attempt_id"), index=True, nullable=False)
    question_id = Column(String(64), nullable=False)
    selected_option = Column(String(8), nullable=True)
    correct_option = Column(String(8), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    response_time_seconds = Column(Float, default=0.0)

    attempt = relationship("QuizAttempt", back_populates="responses")


class TelemetryEvent(Base):
    """
    First-party immutable learning event store.
    Captures all learner actions directly from the website.
    """
    __tablename__ = "telemetry_events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String(64), unique=True, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    student_id = Column(String(64), index=True, nullable=False)
    topic_id = Column(String(64), index=True, nullable=False)
    event_type = Column(String(64), index=True, nullable=False)

    # Contextual optional fields
    attempt_id = Column(String(64), nullable=True)
    question_id = Column(String(64), nullable=True)
    confidence_score = Column(Float, nullable=True)
    selected_option = Column(String(8), nullable=True)
    is_correct = Column(Boolean, nullable=True)
    response_time_seconds = Column(Float, nullable=True)
    quiz_score = Column(Float, nullable=True)
    revision_status = Column(String(32), nullable=True)
    readiness_status = Column(String(32), nullable=True)
    is_synthetic = Column(Boolean, default=False)
