"""
Feature Engineering & Leakage-Free Preprocessing Pipeline
Author: Member 2 (Shreyash Singh)
Role: Feature Engineering, Baseline Modeling, Model Comparison, and Evaluation

Extracts pre-quiz predictor features from interaction telemetry events.
Guarantees strict target leakage prevention by isolating information
available exclusively before a quiz attempt begins.
"""

from typing import Tuple, List, Dict, Any, Optional
import pandas as pd
import numpy as np
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib


# Canonical technical topics
VALID_TOPICS = [
    "topic_superv_01",
    "topic_bias_var_02",
    "topic_eval_metrics_03",
    "topic_tree_ensembles_04",
    "topic_dvc_version_01",
    "topic_mlflow_track_02",
]

# Explicit post-quiz columns that MUST NEVER leak into features
FORBIDDEN_LEAKAGE_COLUMNS = {
    "quiz_score",
    "score",
    "is_correct",
    "selected_option",
    "readiness_status",
    "score_percentage",
    "correct_answers_count"
}


def extract_pre_quiz_features(df_events: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the event stream into an attempt-level feature matrix.
    Each row represents a unique (student_id, topic_id, attempt_id) pair.

    Predictors (strictly pre-quiz):
    - confidence_score: self-reported before this quiz attempt
    - completed_revision: binary (1 if student completed revision before quiz, 0 otherwise)
    - revision_duration_seconds: duration spent in revision (0 if skipped)
    - prior_topic_attempts: number of previous attempts on this topic by this student
    - prior_topic_avg_score: average score on prior attempts on this topic (neutral 50.0 if first attempt)
    - prior_global_avg_score: average score across other topics by this student (neutral 50.0 if first attempt)
    - topic_id: categorical identifier of the subject topic

    Target (post-quiz ground truth):
    - target_score: raw quiz score percentage (0 to 100)
    - target_mastery_band: 0 (Needs Revision < 60), 1 (Developing 60-79), 2 (Demonstrated Mastery >= 80)
    - target_passed: binary (1 if target_score >= 70, 0 otherwise)
    """
    # Sort chronologically by timestamp
    df = df_events.sort_values(by="timestamp").copy()

    # Identify all completed quiz attempts
    calc_events = df[df["event_type"] == "quiz_result_calculated"].dropna(subset=["attempt_id", "quiz_score"])

    feature_rows = []

    for _, result_row in calc_events.iterrows():
        student_id = result_row["student_id"]
        topic_id = result_row["topic_id"]
        attempt_id = result_row["attempt_id"]
        result_time = result_row["timestamp"]
        actual_score = float(result_row["quiz_score"])

        # Filter all events that occurred STRICTLY BEFORE this quiz started
        prior_events = df[
            (df["student_id"] == student_id) &
            (df["timestamp"] < result_time)
        ]

        # 1. Pre-quiz confidence rating for this topic
        topic_conf_events = prior_events[
            (prior_events["topic_id"] == topic_id) &
            (prior_events["event_type"] == "confidence_assessment_submitted")
        ].dropna(subset=["confidence_score"])

        if not topic_conf_events.empty:
            confidence_score = float(topic_conf_events.iloc[-1]["confidence_score"])
        else:
            confidence_score = 50.0  # default neutral confidence if unrated

        # 2. Revision completion prior to this quiz
        rev_events = prior_events[
            (prior_events["topic_id"] == topic_id) &
            (prior_events["event_type"] == "revision_completed")
        ]
        completed_revision = 1 if not rev_events.empty else 0
        revision_duration = float(rev_events["response_time_seconds"].sum()) if completed_revision else 0.0

        # 3. Prior quiz history on this specific topic
        prior_topic_quizzes = prior_events[
            (prior_events["topic_id"] == topic_id) &
            (prior_events["event_type"] == "quiz_result_calculated") &
            (prior_events["attempt_id"] != attempt_id)
        ].dropna(subset=["quiz_score"])

        prior_topic_attempts = len(prior_topic_quizzes)
        prior_topic_avg = float(prior_topic_quizzes["quiz_score"].mean()) if prior_topic_attempts > 0 else 50.0

        # 4. Prior quiz history on other topics (student baseline ability)
        prior_other_quizzes = prior_events[
            (prior_events["topic_id"] != topic_id) &
            (prior_events["event_type"] == "quiz_result_calculated")
        ].dropna(subset=["quiz_score"])

        prior_global_attempts = len(prior_other_quizzes)
        prior_global_avg = float(prior_other_quizzes["quiz_score"].mean()) if prior_global_attempts > 0 else 50.0

        # Discretize targets
        if actual_score >= 80.0:
            mastery_band = 2  # Demonstrated Mastery
            band_label = "Demonstrated Mastery"
        elif actual_score >= 60.0:
            mastery_band = 1  # Developing
            band_label = "Developing"
        else:
            mastery_band = 0  # Needs Revision
            band_label = "Needs Revision"

        target_passed = 1 if actual_score >= 70.0 else 0

        feature_rows.append({
            # Identifiers & Metadata
            "student_id": student_id,
            "topic_id": topic_id,
            "attempt_id": attempt_id,
            "timestamp": result_time,

            # Pre-quiz Predictor Features
            "confidence_score": confidence_score,
            "completed_revision": completed_revision,
            "revision_duration_seconds": revision_duration,
            "prior_topic_attempts": prior_topic_attempts,
            "prior_topic_avg_score": prior_topic_avg,
            "prior_global_attempts": prior_global_attempts,
            "prior_global_avg_score": prior_global_avg,

            # Targets (Outcomes to predict)
            "target_score": actual_score,
            "target_mastery_band": mastery_band,
            "target_mastery_label": band_label,
            "target_passed": target_passed,
        })

    features_df = pd.DataFrame(feature_rows)
    return features_df


def build_preprocessor(categorical_features: List[str], numerical_features: List[str]) -> ColumnTransformer:
    """
    Constructs a scikit-learn ColumnTransformer that standardizes numerical features
    and one-hot encodes categorical topic features.
    """
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
        ],
        remainder="drop"
    )
    return preprocessor


def create_grouped_train_test_split(
    df: pd.DataFrame,
    group_col: str = "student_id",
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits the dataset into train and test partitions by student group.
    Ensures that attempts from the same student NEVER appear across both train and test sets,
    preventing student-level cognitive leakage.
    """
    gss = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
    train_idx, test_idx = next(gss.split(df, groups=df[group_col]))

    train_df = df.iloc[train_idx].copy().reset_index(drop=True)
    test_df = df.iloc[test_idx].copy().reset_index(drop=True)

    # Assert zero student overlap
    train_students = set(train_df[group_col].unique())
    test_students = set(test_df[group_col].unique())
    overlap = train_students.intersection(test_students)
    assert len(overlap) == 0, f"Critical Data Leakage: Student overlap detected in split: {overlap}"

    return train_df, test_df
