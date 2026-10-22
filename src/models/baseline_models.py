import os
import sys

# Ensure project root is in sys.path
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import joblib

from src.features import (
    extract_pre_quiz_features,
    build_preprocessor,
    create_grouped_train_test_split,
    FORBIDDEN_LEAKAGE_COLUMNS
)
from src.evaluation import evaluate_classification_model, compare_models, verify_zero_leakage

TARGET_NAMES = ["Needs Revision", "Developing", "Demonstrated Mastery"]


def get_baseline_classifiers(random_state: int = 42) -> Dict[str, Any]:
    """
    Returns the candidate baseline classification algorithms for Phase 1 comparison.
    """
    return {
        "Dummy (Most Frequent)": DummyClassifier(strategy="most_frequent"),
        "Dummy (Stratified)": DummyClassifier(strategy="stratified", random_state=random_state),
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            C=1.0,
            class_weight="balanced",
            random_state=random_state
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=4,
            min_samples_leaf=4,
            class_weight="balanced",
            random_state=random_state
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            min_samples_leaf=3,
            class_weight="balanced",
            random_state=random_state
        ),
    }


def train_and_compare_baselines(
    df_features: pd.DataFrame,
    target_col: str = "target_mastery_band",
    models_dir: str = "models"
) -> Tuple[pd.DataFrame, Dict[str, Any], Any]:
    """
    Executes the end-to-end baseline comparison:
    1. Verifies zero feature leakage.
    2. Performs group-based train/test splitting (grouped by student_id).
    3. Fits preprocessor on training data only.
    4. Trains all baseline classifiers.
    5. Evaluates on test partition.
    6. Serializes the best performing model artifact.
    """
    os.makedirs(models_dir, exist_ok=True)

    # Define feature subsets
    cat_features = ["topic_id"]
    num_features = [
        "confidence_score",
        "completed_revision",
        "revision_duration_seconds",
        "prior_topic_attempts",
        "prior_topic_avg_score",
        "prior_global_attempts",
        "prior_global_avg_score"
    ]
    feature_cols = cat_features + num_features

    # Verify zero leakage
    verify_zero_leakage(feature_cols, FORBIDDEN_LEAKAGE_COLUMNS)

    # Grouped split by student_id to prevent student-level leakage
    train_df, test_df = create_grouped_train_test_split(df_features, group_col="student_id", test_size=0.25, random_state=42)

    X_train = train_df[feature_cols]
    y_train = train_df[target_col]

    X_test = test_df[feature_cols]
    y_test = test_df[target_col]

    # Preprocessor fitted strictly on training data
    preprocessor = build_preprocessor(cat_features, num_features)

    classifiers = get_baseline_classifiers(random_state=42)
    evaluation_results = {}
    fitted_pipelines = {}

    for name, clf in classifiers.items():
        pipe = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", clf)
        ])

        # Train pipeline
        pipe.fit(X_train, y_train)
        fitted_pipelines[name] = pipe

        # Evaluate on unseen test partition
        metrics = evaluate_classification_model(pipe, X_test, y_test, target_names=TARGET_NAMES)
        evaluation_results[name] = metrics

    comparison_df = compare_models(evaluation_results)

    # Select best model based on Macro F1-Score
    best_model_name = comparison_df.iloc[0]["Model"]
    best_pipeline = fitted_pipelines[best_model_name]

    # Save artifacts
    model_artifact_path = os.path.join(models_dir, "mastery_classifier.joblib")
    joblib.dump(best_pipeline, model_artifact_path)

    # Also save metadata
    metadata_path = os.path.join(models_dir, "model_metadata.json")
    import json
    with open(metadata_path, "w") as f:
        json.dump({
            "best_model": best_model_name,
            "metrics": evaluation_results[best_model_name],
            "feature_columns": feature_cols,
            "target_classes": TARGET_NAMES,
            "is_synthetic": True,
            "train_samples": len(train_df),
            "test_samples": len(test_df)
        }, f, indent=2)

    print(f"Best Model Selected: {best_model_name}")
    print(f"Model artifact saved to: {model_artifact_path}")

    return comparison_df, evaluation_results, best_pipeline


if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    raw_data_path = os.path.join(project_root, "data", "raw", "student_interactions_bootstrap.csv")

    assert os.path.exists(raw_data_path), f"Raw dataset not found at {raw_data_path}"
    df_raw = pd.read_csv(raw_data_path)

    print("Extracting pre-quiz features from interaction event stream...")
    df_feat = extract_pre_quiz_features(df_raw)

    processed_dir = os.path.join(project_root, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    features_csv_path = os.path.join(processed_dir, "pre_quiz_features.csv")
    df_feat.to_csv(features_csv_path, index=False)
    print(f"Features saved to: {features_csv_path} ({len(df_feat)} attempts)")

    print("\nTraining and comparing baseline models...")
    models_dir = os.path.join(project_root, "models")
    comp_df, results, best_pipe = train_and_compare_baselines(df_feat, models_dir=models_dir)

    print("\nModel Comparison Table:")
    print(comp_df.to_string(index=False))
