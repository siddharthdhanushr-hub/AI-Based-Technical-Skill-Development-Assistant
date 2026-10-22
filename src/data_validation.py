"""
Data Acquisition & Schema Validation Module
Author: Member 1 (Shreyas)
Role: Data Acquisition, Data Quality, Schema Validation, and EDA
"""

from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator, ValidationInfo
import pandas as pd
import numpy as np


class EventType(str, Enum):
    TOPIC_SELECTED = "topic_selected"
    CONFIDENCE_ASSESSMENT_SUBMITTED = "confidence_assessment_submitted"
    REVISION_OPENED = "revision_opened"
    REVISION_COMPLETED = "revision_completed"
    QUIZ_STARTED = "quiz_started"
    QUESTION_ANSWERED = "question_answered"
    QUIZ_SUBMITTED = "quiz_submitted"
    QUIZ_RESULT_CALCULATED = "quiz_result_calculated"
    TOPIC_REASSESSED = "topic_reassessed"
    RECOMMENDATION_DISPLAYED = "recommendation_displayed"


class ReadinessBand(str, Enum):
    NOT_ASSESSED = "Not Yet Assessed"
    NEEDS_REVISION = "Needs Revision"
    DEVELOPING = "Developing"
    NEARLY_READY = "Nearly Ready"
    STRONG_MASTERY = "Demonstrated Mastery"


class LearningInteractionEvent(BaseModel):
    """
    Schema for a single first-party student learning event.
    Supports both real student telemetry and documented bootstrap data.
    """
    event_id: str = Field(..., description="Unique event identifier (e.g. ev_... or UUID)")
    timestamp: datetime = Field(..., description="ISO 8601 UTC timestamp of the event")
    student_id: str = Field(..., min_length=3, description="Pseudonymous learner identifier")
    topic_id: str = Field(..., min_length=3, description="Technical topic slug/identifier")
    event_type: EventType = Field(..., description="Type of user journey action")

    # Optional fields depending on event_type
    attempt_id: Optional[str] = Field(None, description="Quiz attempt identifier")
    question_id: Optional[str] = Field(None, description="Question identifier")
    confidence_score: Optional[float] = Field(None, ge=0.0, le=100.0, description="Self-reported confidence 0-100")
    selected_option: Optional[str] = Field(None, description="Selected option A, B, C, D")
    is_correct: Optional[bool] = Field(None, description="Correctness flag")
    response_time_seconds: Optional[float] = Field(None, ge=0.0, description="Response time in seconds")
    quiz_score: Optional[float] = Field(None, ge=0.0, le=100.0, description="Attempt score percentage 0-100")
    revision_status: Optional[str] = Field(None, description="Revision status: opened, completed")
    readiness_status: Optional[str] = Field(None, description="Calculated readiness category")
    is_synthetic: bool = Field(False, description="Explicit flag: True if bootstrap synthetic, False if real")

    @field_validator("selected_option")
    @classmethod
    def validate_option(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v_upper = v.upper()
            if v_upper not in {"A", "B", "C", "D"}:
                raise ValueError(f"selected_option must be one of ['A', 'B', 'C', 'D'], got {v}")
            return v_upper
        return v


class DataQualityReport(BaseModel):
    """Structured report summarizing dataset quality validation findings."""
    total_records: int
    is_synthetic_ratio: float
    unique_students: int
    unique_topics: int
    duplicate_event_ids: int
    missing_value_summary: Dict[str, int]
    invalid_range_counts: Dict[str, int]
    event_type_distribution: Dict[str, int]
    confidence_stats: Dict[str, float]
    quiz_score_stats: Dict[str, float]
    confidence_quiz_correlation: Optional[float]
    validation_status: str  # "PASSED", "WARNING", "FAILED"
    issues_detected: List[str]


class DataQualityValidator:
    """
    Validates batch datasets of student interaction telemetry.
    Ensures data integrity, checks missing values, detects duplicates,
    and inspects correlation between confidence ratings and quiz outcomes.
    """

    REQUIRED_COLUMNS = [
        "event_id", "timestamp", "student_id", "topic_id", "event_type", "is_synthetic"
    ]

    ALLOWED_EVENT_TYPES = {e.value for e in EventType}

    @classmethod
    def validate_dataframe(cls, df: pd.DataFrame) -> DataQualityReport:
        issues: List[str] = []

        # 1. Column completeness
        missing_cols = [c for c in cls.REQUIRED_COLUMNS if c not in df.columns]
        if missing_cols:
            issues.append(f"Missing mandatory columns: {missing_cols}")
            return DataQualityReport(
                total_records=len(df),
                is_synthetic_ratio=0.0,
                unique_students=0,
                unique_topics=0,
                duplicate_event_ids=0,
                missing_value_summary={},
                invalid_range_counts={},
                event_type_distribution={},
                confidence_stats={},
                quiz_score_stats={},
                confidence_quiz_correlation=None,
                validation_status="FAILED",
                issues_detected=issues
            )

        # 2. Check duplicate event IDs
        dup_count = int(df["event_id"].duplicated().sum())
        if dup_count > 0:
            issues.append(f"Found {dup_count} duplicate event_ids.")

        # 3. Check invalid event types
        invalid_events = df[~df["event_type"].isin(cls.ALLOWED_EVENT_TYPES)]
        if not invalid_events.empty:
            issues.append(f"Found {len(invalid_events)} records with unregistered event_type.")

        # 4. Check ranges
        invalid_ranges: Dict[str, int] = {}
        if "confidence_score" in df.columns:
            invalid_conf = df["confidence_score"].dropna().apply(lambda x: x < 0.0 or x > 100.0).sum()
            invalid_ranges["confidence_score"] = int(invalid_conf)
            if invalid_conf > 0:
                issues.append(f"Found {invalid_conf} confidence scores outside [0, 100].")

        if "quiz_score" in df.columns:
            invalid_quiz = df["quiz_score"].dropna().apply(lambda x: x < 0.0 or x > 100.0).sum()
            invalid_ranges["quiz_score"] = int(invalid_quiz)
            if invalid_quiz > 0:
                issues.append(f"Found {invalid_quiz} quiz scores outside [0, 100].")

        if "response_time_seconds" in df.columns:
            invalid_time = df["response_time_seconds"].dropna().apply(lambda x: x < 0.0).sum()
            invalid_ranges["response_time_seconds"] = int(invalid_time)
            if invalid_time > 0:
                issues.append(f"Found {invalid_time} negative response times.")

        # 5. Missing values
        missing_summary = {col: int(df[col].isna().sum()) for col in df.columns}

        # 6. Distributions
        event_dist = {str(k): int(v) for k, v in df["event_type"].value_counts().items()}

        # 7. Summary statistics
        conf_series = df["confidence_score"].dropna()
        conf_stats = {
            "mean": float(conf_series.mean()) if not conf_series.empty else 0.0,
            "std": float(conf_series.std()) if len(conf_series) > 1 else 0.0,
            "min": float(conf_series.min()) if not conf_series.empty else 0.0,
            "max": float(conf_series.max()) if not conf_series.empty else 0.0,
        }

        quiz_series = df["quiz_score"].dropna()
        quiz_stats = {
            "mean": float(quiz_series.mean()) if not quiz_series.empty else 0.0,
            "std": float(quiz_series.std()) if len(quiz_series) > 1 else 0.0,
            "min": float(quiz_series.min()) if not quiz_series.empty else 0.0,
            "max": float(quiz_series.max()) if not quiz_series.empty else 0.0,
        }

        # 8. Correlation between confidence and quiz outcome
        correlation = None
        # Pair confidence and quiz scores per student/topic attempt
        conf_df = df[df["event_type"] == EventType.CONFIDENCE_ASSESSMENT_SUBMITTED.value][
            ["student_id", "topic_id", "confidence_score"]
        ].dropna()
        quiz_df = df[df["event_type"] == EventType.QUIZ_RESULT_CALCULATED.value][
            ["student_id", "topic_id", "quiz_score"]
        ].dropna()

        if not conf_df.empty and not quiz_df.empty:
            merged = pd.merge(conf_df, quiz_df, on=["student_id", "topic_id"])
            if len(merged) >= 5:
                corr_val = merged["confidence_score"].corr(merged["quiz_score"])
                correlation = float(round(corr_val, 4)) if not np.isnan(corr_val) else 0.0

        # Synthetic ratio
        synthetic_ratio = float(df["is_synthetic"].mean()) if "is_synthetic" in df.columns else 0.0
        if synthetic_ratio > 0.0:
            issues.append(f"Note: Dataset contains {synthetic_ratio*100:.1f}% synthetic bootstrap records.")

        status = "PASSED"
        if dup_count > 0 or any(v > 0 for v in invalid_ranges.values()):
            status = "FAILED"
        elif issues:
            status = "WARNING"

        return DataQualityReport(
            total_records=len(df),
            is_synthetic_ratio=round(synthetic_ratio, 4),
            unique_students=int(df["student_id"].nunique()),
            unique_topics=int(df["topic_id"].nunique()),
            duplicate_event_ids=dup_count,
            missing_value_summary=missing_summary,
            invalid_range_counts=invalid_ranges,
            event_type_distribution=event_dist,
            confidence_stats=conf_stats,
            quiz_score_stats=quiz_stats,
            confidence_quiz_correlation=correlation,
            validation_status=status,
            issues_detected=issues
        )


if __name__ == "__main__":
    import os
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_path = os.path.join(project_root, "data", "raw", "student_interactions_bootstrap.csv")
    out_dir = os.path.join(project_root, "reports")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "data_validation_report.json")

    print(f"Loading raw interactions from {data_path}...")
    df = pd.read_csv(data_path)
    report = DataQualityValidator.validate_dataframe(df)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report.model_dump_json(indent=2))

    print(f"Validation status: {report.validation_status}")
    print(f"Total records validated: {report.total_records}")
    print(f"Validation report saved to: {out_path}")

