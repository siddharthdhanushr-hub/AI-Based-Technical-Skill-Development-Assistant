"""
Unit & Integration Tests for Feature Engineering & Baseline Models
Author: Member 2 (Shreyash Singh)
Role: Feature Engineering, Baseline Modeling, Model Comparison, and Evaluation
"""

import os
import pytest
import pandas as pd
import numpy as np

from src.features import (
    extract_pre_quiz_features,
    build_preprocessor,
    create_grouped_train_test_split,
    FORBIDDEN_LEAKAGE_COLUMNS
)
from src.evaluation import (
    evaluate_classification_model,
    compare_models,
    verify_zero_leakage
)
from src.models.baseline_models import get_baseline_classifiers, train_and_compare_baselines
from src.models.predictor import MasteryPredictor


@pytest.fixture
def sample_events_df():
    """Provides a synthetic sequence of events for testing feature extraction."""
    return pd.DataFrame([
        # Student 1 - Topic 1
        {"event_id": "ev_01", "timestamp": "2026-10-01T10:00:00Z", "student_id": "std_01", "topic_id": "topic_superv_01", "event_type": "topic_selected", "confidence_score": None, "quiz_score": None, "attempt_id": None, "response_time_seconds": None, "is_synthetic": True},
        {"event_id": "ev_02", "timestamp": "2026-10-01T10:01:00Z", "student_id": "std_01", "topic_id": "topic_superv_01", "event_type": "confidence_assessment_submitted", "confidence_score": 45.0, "quiz_score": None, "attempt_id": None, "response_time_seconds": None, "is_synthetic": True},
        {"event_id": "ev_03", "timestamp": "2026-10-01T10:02:00Z", "student_id": "std_01", "topic_id": "topic_superv_01", "event_type": "revision_completed", "confidence_score": None, "quiz_score": None, "attempt_id": None, "response_time_seconds": 120.0, "is_synthetic": True},
        {"event_id": "ev_04", "timestamp": "2026-10-01T10:05:00Z", "student_id": "std_01", "topic_id": "topic_superv_01", "event_type": "quiz_result_calculated", "confidence_score": None, "quiz_score": 80.0, "attempt_id": "att_01", "response_time_seconds": None, "is_synthetic": True},

        # Student 2 - Topic 1
        {"event_id": "ev_05", "timestamp": "2026-10-01T11:00:00Z", "student_id": "std_02", "topic_id": "topic_superv_01", "event_type": "confidence_assessment_submitted", "confidence_score": 85.0, "quiz_score": None, "attempt_id": None, "response_time_seconds": None, "is_synthetic": True},
        {"event_id": "ev_06", "timestamp": "2026-10-01T11:05:00Z", "student_id": "std_02", "topic_id": "topic_superv_01", "event_type": "quiz_result_calculated", "confidence_score": None, "quiz_score": 90.0, "attempt_id": "att_02", "response_time_seconds": None, "is_synthetic": True},

        # Student 3 - Topic 2
        {"event_id": "ev_07", "timestamp": "2026-10-01T12:00:00Z", "student_id": "std_03", "topic_id": "topic_bias_var_02", "event_type": "confidence_assessment_submitted", "confidence_score": 30.0, "quiz_score": None, "attempt_id": None, "response_time_seconds": None, "is_synthetic": True},
        {"event_id": "ev_08", "timestamp": "2026-10-01T12:05:00Z", "student_id": "std_03", "topic_id": "topic_bias_var_02", "event_type": "quiz_result_calculated", "confidence_score": None, "quiz_score": 40.0, "attempt_id": "att_03", "response_time_seconds": None, "is_synthetic": True},
    ])


class TestFeatureEngineering:

    def test_extract_pre_quiz_features(self, sample_events_df):
        features = extract_pre_quiz_features(sample_events_df)
        assert len(features) == 3
        assert "confidence_score" in features.columns
        assert "completed_revision" in features.columns
        assert "prior_topic_attempts" in features.columns
        assert "target_mastery_band" in features.columns

        # Verify Student 1 values
        s1 = features[features["student_id"] == "std_01"].iloc[0]
        assert s1["confidence_score"] == 45.0
        assert s1["completed_revision"] == 1
        assert s1["revision_duration_seconds"] == 120.0
        assert s1["target_mastery_band"] == 2  # 80% = Demonstrated Mastery

    def test_target_leakage_prevention(self):
        # Ensure forbidden post-quiz outcome fields cannot leak into predictor set
        clean_features = ["confidence_score", "completed_revision", "topic_id"]
        assert verify_zero_leakage(clean_features, FORBIDDEN_LEAKAGE_COLUMNS) is True

        dirty_features = ["confidence_score", "quiz_score", "topic_id"]
        with pytest.raises(ValueError, match="CRITICAL TARGET LEAKAGE"):
            verify_zero_leakage(dirty_features, FORBIDDEN_LEAKAGE_COLUMNS)

    def test_grouped_train_test_split_independence(self):
        df_dummy = pd.DataFrame({
            "student_id": ["s1", "s1", "s2", "s2", "s3", "s3", "s4", "s4"],
            "feat": [1, 2, 3, 4, 5, 6, 7, 8],
            "target": [0, 1, 0, 1, 0, 1, 0, 1]
        })
        train_df, test_df = create_grouped_train_test_split(df_dummy, group_col="student_id", test_size=0.5, random_state=42)

        train_students = set(train_df["student_id"].unique())
        test_students = set(test_df["student_id"].unique())
        assert len(train_students.intersection(test_students)) == 0


class TestModelTrainingAndEvaluation:

    def test_baseline_classifiers_dictionary(self):
        clfs = get_baseline_classifiers(random_state=42)
        assert "Dummy (Most Frequent)" in clfs
        assert "Logistic Regression" in clfs
        assert "Decision Tree" in clfs
        assert "Random Forest" in clfs

    def test_model_artifact_exists_and_loads(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        artifact_path = os.path.join(project_root, "models", "mastery_classifier.joblib")
        assert os.path.exists(artifact_path), f"Trained model artifact missing at {artifact_path}"

        predictor = MasteryPredictor(model_path=artifact_path)
        assert predictor.model is not None

        # Test inference
        res = predictor.predict_readiness(
            student_id="std_test_01",
            topic_id="topic_superv_01",
            confidence_score=75.0,
            completed_revision=True,
            prior_topic_attempts=1,
            prior_topic_avg_score=70.0
        )

        assert res["predicted_band"] in ["Needs Revision", "Developing", "Demonstrated Mastery"]
        assert res["is_fallback"] is False
        assert "class_probabilities" in res
        assert "recommended_action" in res

    def test_predictor_fallback_path(self):
        # Force fallback by pointing to non-existent model path
        predictor = MasteryPredictor(model_path="non_existent_model_file.joblib")
        assert predictor.model is None

        res = predictor.predict_readiness(
            student_id="std_test_02",
            topic_id="topic_superv_01",
            confidence_score=35.0,
            completed_revision=False,
            prior_topic_attempts=0
        )

        assert res["is_fallback"] is True
        assert res["model_source"] == "calibrated_rule_fallback"
        assert res["predicted_band"] == "Needs Revision"
        assert "flashcards" in res["recommended_action"].lower()
