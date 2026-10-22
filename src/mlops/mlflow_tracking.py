"""
MLflow Experiment Tracking and Model Registry Service
Author: Member 4 (Siddharth Dhanush R, Project Lead)
Role: Backend API, MLflow Tracking, DVC Pipeline, System Integration, and Documentation

Logs hyperparameters, GroupShuffleSplit metrics, classification reports,
and serialized scikit-learn pipelines into MLflow.
"""

import os
import sys
import json
from typing import Dict, Any, Tuple

# Silence MLflow assistant hint before importing and allow file store
os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"

# Ensure project root is on sys.path
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import pandas as pd
import numpy as np
import joblib
import mlflow
import mlflow.sklearn

from src.features import (
    build_preprocessor,
    create_grouped_train_test_split,
    FORBIDDEN_LEAKAGE_COLUMNS
)
from src.evaluation import evaluate_classification_model, compare_models, verify_zero_leakage
from src.models.baseline_models import get_baseline_classifiers, TARGET_NAMES


EXPERIMENT_NAME = "technical_skill_mastery_baselines"


def run_tracked_experiments(
    features_csv_path: str = None,
    experiment_name: str = EXPERIMENT_NAME,
    random_state: int = 42
) -> Tuple[pd.DataFrame, str]:
    """
    Executes baseline model training under MLflow tracking:
    - Logs parameters, metrics (Accuracy, Macro-F1, Class F1s), tags.
    - Persists models into MLflow artifact store.
    - Exports best model to models/mastery_classifier.joblib.
    - Saves metrics summary to reports/model_metrics.json.
    """
    project_root = _project_root
    if features_csv_path is None:
        features_csv_path = os.path.join(project_root, "data", "processed", "pre_quiz_features.csv")

    assert os.path.exists(features_csv_path), f"Processed features not found at {features_csv_path}"
    df_features = pd.read_csv(features_csv_path)

    # Configure local MLflow tracking
    tracking_dir = os.path.join(project_root, "mlruns")
    os.makedirs(tracking_dir, exist_ok=True)
    mlflow.set_tracking_uri(f"file:///{os.path.abspath(tracking_dir).replace(os.sep, '/')}")
    mlflow.set_experiment(experiment_name)

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

    # Zero leakage validation
    verify_zero_leakage(feature_cols, FORBIDDEN_LEAKAGE_COLUMNS)

    # Grouped split by student_id
    train_df, test_df = create_grouped_train_test_split(
        df_features, group_col="student_id", test_size=0.25, random_state=random_state
    )

    X_train = train_df[feature_cols]
    y_train = train_df["target_mastery_band"]
    X_test = test_df[feature_cols]
    y_test = test_df["target_mastery_band"]

    preprocessor = build_preprocessor(cat_features, num_features)
    classifiers = get_baseline_classifiers(random_state=random_state)

    evaluation_results = {}
    fitted_pipelines = {}
    run_ids = {}

    print(f"=== Starting MLflow Experiment: '{experiment_name}' ===")
    print(f"Tracking URI: {mlflow.get_tracking_uri()}")
    print(f"Training Samples: {len(train_df)} | Test Samples: {len(test_df)}")

    for model_name, clf in classifiers.items():
        from sklearn.pipeline import Pipeline
        pipe = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", clf)
        ])

        with mlflow.start_run(run_name=model_name) as run:
            run_ids[model_name] = run.info.run_id

            # Fit pipeline strictly on train data
            pipe.fit(X_train, y_train)
            fitted_pipelines[model_name] = pipe

            # Evaluate on held-out test students
            metrics = evaluate_classification_model(pipe, X_test, y_test, target_names=TARGET_NAMES)
            evaluation_results[model_name] = metrics

            # Log Hyperparameters
            clf_params = clf.get_params()
            for p_name, p_val in clf_params.items():
                if isinstance(p_val, (int, float, str, bool)):
                    mlflow.log_param(f"clf_{p_name}", p_val)

            mlflow.log_param("test_size", 0.25)
            mlflow.log_param("split_strategy", "GroupShuffleSplit_by_student_id")
            mlflow.log_param("features_count", len(feature_cols))

            # Log Metrics
            mlflow.log_metric("accuracy", metrics["accuracy"])
            mlflow.log_metric("balanced_accuracy", metrics["balanced_accuracy"])
            mlflow.log_metric("f1_macro", metrics["f1_macro"])
            mlflow.log_metric("f1_weighted", metrics["f1_weighted"])
            mlflow.log_metric("precision_macro", metrics["precision_macro"])
            mlflow.log_metric("recall_macro", metrics["recall_macro"])

            report_dict = metrics.get("classification_report", {})
            for cls_name in TARGET_NAMES:
                if cls_name in report_dict:
                    safe_name = f"f1_{cls_name.lower().replace(' ', '_')}"
                    mlflow.log_metric(safe_name, report_dict[cls_name].get("f1-score", 0.0))

            # Log Academic Integrity & MLOps Tags
            mlflow.set_tag("author", "Siddharth Dhanush R")
            mlflow.set_tag("model_family", clf.__class__.__name__)
            mlflow.set_tag("is_synthetic", "True")
            mlflow.set_tag("leakage_free", "True")
            mlflow.set_tag("group_col", "student_id")

            # Log scikit-learn model artifact using cloudpickle format
            try:
                mlflow.sklearn.log_model(
                    sk_model=pipe,
                    name="model",
                    serialization_format="cloudpickle"
                )
            except Exception as e:
                # Fallback to pickle if needed
                mlflow.sklearn.log_model(
                    sk_model=pipe,
                    name="model",
                    serialization_format="pickle"
                )

            print(f"Logged run: {model_name} (Macro F1: {metrics['f1_macro']:.4f}, Accuracy: {metrics['accuracy']:.4f})")

    comparison_df = compare_models(evaluation_results)
    best_model_name = comparison_df.iloc[0]["Model"]
    best_pipeline = fitted_pipelines[best_model_name]
    best_run_id = run_ids[best_model_name]

    # Tag the champion run
    with mlflow.start_run(run_id=best_run_id):
        mlflow.set_tag("is_champion", "True")
        mlflow.set_tag("deployment_candidate", "production_candidate")

    # Save best model to models/
    models_dir = os.path.join(project_root, "models")
    os.makedirs(models_dir, exist_ok=True)
    joblib_path = os.path.join(models_dir, "mastery_classifier.joblib")
    joblib.dump(best_pipeline, joblib_path)

    metadata_path = os.path.join(models_dir, "model_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump({
            "best_model": best_model_name,
            "best_run_id": best_run_id,
            "experiment_name": experiment_name,
            "metrics": evaluation_results[best_model_name],
            "feature_columns": feature_cols,
            "target_classes": TARGET_NAMES,
            "is_synthetic": True,
            "leakage_free": True,
            "split_group": "student_id",
            "train_samples": len(train_df),
            "test_samples": len(test_df)
        }, f, indent=2)

    # Export report metrics for DVC tracking
    reports_dir = os.path.join(project_root, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    metrics_path = os.path.join(reports_dir, "model_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump({
            "champion_model": best_model_name,
            "champion_macro_f1": evaluation_results[best_model_name]["f1_macro"],
            "champion_accuracy": evaluation_results[best_model_name]["accuracy"],
            "champion_weighted_f1": evaluation_results[best_model_name]["f1_weighted"],
            "all_models": {
                name: {
                    "macro_f1": m["f1_macro"],
                    "accuracy": m["accuracy"]
                } for name, m in evaluation_results.items()
            }
        }, f, indent=2)

    print(f"\nChampion Model: {best_model_name} (Run ID: {best_run_id})")
    print(f"Artifacts saved to {joblib_path} and {metrics_path}")

    return comparison_df, best_model_name


if __name__ == "__main__":
    comp_df, champion = run_tracked_experiments()
    print("\nSummary Comparison Table:")
    print(comp_df.to_string(index=False))
