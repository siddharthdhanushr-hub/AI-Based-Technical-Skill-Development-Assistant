from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


# 1. Curriculum
class SubjectOut(BaseModel):
    subject_id: str
    subject_name: str
    description: str
    topics_count: int


class TopicOut(BaseModel):
    topic_id: str
    topic_name: str
    subject_id: str
    description: str
    difficulty: str
    estimated_minutes: int


# 2. Confidence Assessment
class ConfidenceSubmitIn(BaseModel):
    student_id: str = Field(..., min_length=2)
    topic_id: str = Field(..., min_length=2)
    confidence_score: float = Field(..., ge=0.0, le=100.0)
    notes: Optional[str] = None


class ConfidenceSubmitOut(BaseModel):
    assessment_id: str
    student_id: str
    topic_id: str
    confidence_score: float
    confidence_band: str
    needs_revision: bool
    threshold_applied: float
    timestamp: datetime


# 3. Revision
class DefinitionItem(BaseModel):
    term: str
    definition: str


class FlashcardItem(BaseModel):
    card_id: str
    front: str
    back: str


class RevisionOut(BaseModel):
    topic_id: str
    topic_name: str
    summary: str
    key_definitions: List[DefinitionItem]
    flashcards: List[FlashcardItem]


class RevisionCompleteIn(BaseModel):
    student_id: str
    topic_id: str
    cards_reviewed_count: int = 0
    duration_seconds: float = 0.0


class RevisionCompleteOut(BaseModel):
    status: str
    recorded_at: datetime


# 4. Quiz Engine
class QuestionOut(BaseModel):
    question_id: str
    text: str
    options: List[str]


class QuizStartIn(BaseModel):
    student_id: str
    topic_id: str


class QuizStartOut(BaseModel):
    attempt_id: str
    topic_id: str
    questions: List[QuestionOut]


class AnswerItem(BaseModel):
    question_id: str
    selected_option: str
    response_time_seconds: float = 0.0


class QuizSubmitIn(BaseModel):
    attempt_id: str
    student_id: str
    topic_id: str
    answers: List[AnswerItem]


class QuestionFeedbackItem(BaseModel):
    question_id: str
    selected_option: Optional[str]
    correct_option: str
    is_correct: bool
    explanation: str


class QuizSubmitOut(BaseModel):
    attempt_id: str
    topic_id: str
    score_percentage: float
    total_questions: int
    correct_count: int
    detailed_feedback: List[QuestionFeedbackItem]
    readiness_status: str
    recommended_action: str


# 5. Readiness & Progress
class TopicReadinessOut(BaseModel):
    student_id: str
    topic_id: str
    confidence_score: Optional[float]
    confidence_band: str
    latest_quiz_score: Optional[float]
    best_quiz_score: Optional[float]
    attempts_count: int
    revision_completed: bool
    readiness_status: str
    recommended_next_action: str


class ProgressSummaryOut(BaseModel):
    student_id: str
    topics_assessed: int
    weak_topics_count: int
    quizzes_taken: int
    average_quiz_score: float
    topic_readiness_breakdown: List[TopicReadinessOut]


# 6. Telemetry
class TelemetryEventIn(BaseModel):
    event_id: str
    timestamp: datetime
    student_id: str
    topic_id: str
    event_type: str
    attempt_id: Optional[str] = None
    question_id: Optional[str] = None
    confidence_score: Optional[float] = None
    selected_option: Optional[str] = None
    is_correct: Optional[bool] = None
    response_time_seconds: Optional[float] = None
    quiz_score: Optional[float] = None
    revision_status: Optional[str] = None
    readiness_status: Optional[str] = None
    is_synthetic: bool = False


# 7. Model Inference
class PredictMasteryIn(BaseModel):
    student_id: str
    topic_id: str
    confidence_score: float = Field(..., ge=0.0, le=100.0)
    completed_revision: bool = False
    revision_duration_seconds: float = 0.0
    prior_topic_attempts: int = 0
    prior_topic_avg_score: float = 50.0


class PredictMasteryOut(BaseModel):
    student_id: str
    topic_id: str
    predicted_band: str
    class_probabilities: Dict[str, float]
    model_source: str
    is_fallback: bool
    recommended_action: str
