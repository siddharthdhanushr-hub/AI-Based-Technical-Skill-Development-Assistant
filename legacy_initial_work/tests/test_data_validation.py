"""
Unit & Integration Tests for Data Validation & Quality Checks
Author: Member 1 (Shreyas)
Role: Data Acquisition, Data Quality, Schema Validation, and EDA
"""

import os
import pytest
import pandas as pd
from datetime import datetime
from pydantic import ValidationError

from src.data_validation import (
    LearningInteractionEvent,
    EventType,
    DataQualityValidator,
    DataQualityReport
)


class TestSingleEventValidation:
    """Tests Pydantic schema validation on individual learning interaction events."""

    def test_valid_confidence_event(self):
        event = LearningInteractionEvent(
            event_id="ev_test_001",
            timestamp=datetime.utcnow(),
            student_id="std_sim_001",
            topic_id="topic_superv_01",
            event_type=EventType.CONFIDENCE_ASSESSMENT_SUBMITTED,
            confidence_score=75.5,
            is_synthetic=True
        )
        assert event.confidence_score == 75.5
        assert event.event_type == EventType.CONFIDENCE_ASSESSMENT_SUBMITTED
        assert event.is_synthetic is True

    def test_invalid_confidence_score_out_of_bounds(self):
        # Confidence score > 100 should be rejected
        with pytest.raises(ValidationError):
            LearningInteractionEvent(
                event_id="ev_test_002",
                timestamp=datetime.utcnow(),
                student_id="std_sim_001",
                topic_id="topic_superv_01",
                event_type=EventType.CONFIDENCE_ASSESSMENT_SUBMITTED,
                confidence_score=110.0
            )

        # Confidence score < 0 should be rejected
        with pytest.raises(ValidationError):
            LearningInteractionEvent(
                event_id="ev_test_003",
                timestamp=datetime.utcnow(),
                student_id="std_sim_001",
                topic_id="topic_superv_01",
                event_type=EventType.CONFIDENCE_ASSESSMENT_SUBMITTED,
                confidence_score=-5.0
            )

    def test_valid_question_answered_event(self):
        event = LearningInteractionEvent(
            event_id="ev_test_004",
            timestamp=datetime.utcnow(),
            student_id="std_sim_002",
            topic_id="topic_bias_var_02",
            event_type=EventType.QUESTION_ANSWERED,
            attempt_id="att_001",
            question_id="q_bv_01",
            selected_option="b",  # lower case
            is_correct=True,
            response_time_seconds=24.5,
            is_synthetic=True
        )
        assert event.selected_option == "B"  # normalized to uppercase
        assert event.response_time_seconds == 24.5

    def test_invalid_option_choice(self):
        with pytest.raises(ValidationError):
            LearningInteractionEvent(
                event_id="ev_test_005",
                timestamp=datetime.utcnow(),
                student_id="std_sim_002",
                topic_id="topic_bias_var_02",
                event_type=EventType.QUESTION_ANSWERED,
                selected_option="E"  # Not in A, B, C, D
            )

    def test_negative_response_time_rejected(self):
        with pytest.raises(ValidationError):
            LearningInteractionEvent(
                event_id="ev_test_006",
                timestamp=datetime.utcnow(),
                student_id="std_sim_002",
                topic_id="topic_bias_var_02",
                event_type=EventType.QUESTION_ANSWERED,
                response_time_seconds=-10.0
            )


class TestDatasetQualityValidator:
    """Tests batch quality validator across synthetic and edge-case datasets."""

    @pytest.fixture
    def sample_clean_df(self):
        return pd.DataFrame([
            {
                "event_id": f"ev_{i:03d}",
                "timestamp": "2026-10-23T01:00:00Z",
                "student_id": f"std_{i % 5:02d}",
                "topic_id": "topic_superv_01",
                "event_type": "confidence_assessment_submitted" if i % 2 == 0 else "quiz_result_calculated",
                "confidence_score": 70.0 if i % 2 == 0 else None,
                "quiz_score": 80.0 if i % 2 == 1 else None,
                "response_time_seconds": 30.0 if i % 2 == 1 else None,
                "is_synthetic": True
            }
            for i in range(20)
        ])

    def test_sample_clean_dataframe_validation(self, sample_clean_df):
        report = DataQualityValidator.validate_dataframe(sample_clean_df)
        assert isinstance(report, DataQualityReport)
        assert report.total_records == 20
        assert report.duplicate_event_ids == 0
        assert report.is_synthetic_ratio == 1.0
        assert report.validation_status in {"PASSED", "WARNING"}

    def test_duplicate_event_ids_detected(self, sample_clean_df):
        # Inject duplicate ID
        dirty_df = sample_clean_df.copy()
        dirty_df.loc[1, "event_id"] = dirty_df.loc[0, "event_id"]

        report = DataQualityValidator.validate_dataframe(dirty_df)
        assert report.duplicate_event_ids == 1
        assert report.validation_status == "FAILED"
        assert any("duplicate" in issue.lower() for issue in report.issues_detected)

    def test_out_of_bounds_score_detected(self, sample_clean_df):
        dirty_df = sample_clean_df.copy()
        dirty_df.loc[0, "confidence_score"] = 150.0  # Invalid range

        report = DataQualityValidator.validate_dataframe(dirty_df)
        assert report.invalid_range_counts.get("confidence_score") == 1
        assert report.validation_status == "FAILED"

    def test_missing_mandatory_columns(self):
        incomplete_df = pd.DataFrame([{"student_id": "std_01"}])
        report = DataQualityValidator.validate_dataframe(incomplete_df)
        assert report.validation_status == "FAILED"
        assert any("missing mandatory columns" in issue.lower() for issue in report.issues_detected)

    def test_bootstrap_dataset_file_integrity(self):
        """Verifies the generated bootstrap CSV passes all quality and schema checks."""
        csv_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data", "raw", "student_interactions_bootstrap.csv"
        )
        assert os.path.exists(csv_path), f"Bootstrap dataset file not found at {csv_path}"

        df = pd.read_csv(csv_path)
        report = DataQualityValidator.validate_dataframe(df)

        assert report.total_records >= 1000
        assert report.unique_students >= 20
        assert report.duplicate_event_ids == 0
        assert report.invalid_range_counts.get("confidence_score", 0) == 0
        assert report.invalid_range_counts.get("quiz_score", 0) == 0
        assert report.invalid_range_counts.get("response_time_seconds", 0) == 0
        assert report.is_synthetic_ratio == 1.0  # Explicitly marked as synthetic
        assert report.confidence_quiz_correlation is not None
        assert report.validation_status in {"PASSED", "WARNING"}
