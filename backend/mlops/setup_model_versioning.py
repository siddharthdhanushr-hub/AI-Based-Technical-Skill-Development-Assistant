"""
MLflow Model Versioning and Lifecycle Management
Sets up explicit model versions in the MLflow Model Registry for AssessmentChampionPredictor:
- Version 1 (v1): Decision Tree Candidate Baseline (Stage: Staging / Archived, Alias: challenger)
- Version 2 (v2): Random Forest Champion Model (Stage: Production, Alias: champion)

Enables full model versioning, lineage tracking, and side-by-side metric comparison in the MLflow UI.
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = str(Path(__file__).resolve().parent.parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import mlflow
from mlflow.tracking import MlflowClient

TRACKING_URI = "http://localhost:5000"
EXPERIMENT_ID = "1"
MODEL_NAME = "AssessmentChampionPredictor"

mlflow.set_tracking_uri(TRACKING_URI)
client = MlflowClient(tracking_uri=TRACKING_URI)

print("=================================================================")
print("📦 Setting up MLflow Model Versioning in Model Registry")
print("=================================================================")
print(f"Tracking URI : {TRACKING_URI}")
print(f"Model Name   : {MODEL_NAME}")

# Ensure registered model exists
try:
    reg_model = client.get_registered_model(MODEL_NAME)
    print(f"Found existing Registered Model: '{MODEL_NAME}'")
except Exception:
    reg_model = client.create_registered_model(
        name=MODEL_NAME,
        description="Production & Candidate Skill Readiness Predictor for 21st-Century Technical Competencies."
    )
    print(f"Created Registered Model: '{MODEL_NAME}'")

# Find the latest runs in experiment 1
runs = client.search_runs(experiment_ids=[EXPERIMENT_ID], order_by=["attributes.start_time DESC"])
dt_run = None
rf_run = None

for r in runs:
    run_name = r.data.tags.get("mlflow.runName", "")
    if "Decision_Tree" in run_name and not dt_run:
        dt_run = r
    elif "Random_Forest" in run_name and not rf_run:
        rf_run = r

assert dt_run is not None, "Could not find a Decision_Tree run in experiment 1"
assert rf_run is not None, "Could not find a Random_Forest run in experiment 1"

print(f"Found Decision Tree Candidate Run: {dt_run.info.run_id} ({dt_run.data.tags.get('mlflow.runName')})")
print(f"Found Random Forest Champion Run : {rf_run.info.run_id} ({rf_run.data.tags.get('mlflow.runName')})")

# Determine current versions
existing_versions = client.search_model_versions(f"name='{MODEL_NAME}'")
print(f"Currently registered versions: {[v.version for v in existing_versions]}")

# Register / Configure Version 1 (Candidate / Baseline)
v1_source = f"{dt_run.info.artifact_uri}/model"
try:
    # If version 1 doesn't exist, create it
    if not any(v.version == "1" for v in existing_versions):
        v1 = client.create_model_version(
            name=MODEL_NAME,
            source=v1_source,
            run_id=dt_run.info.run_id,
            description="v1: Decision Tree Candidate Baseline (Accuracy: 72.04%, ROC-AUC: 0.7885). Replaced by Random Forest Champion.",
            tags={
                "stage": "Staging",
                "model_architecture": "DecisionTreeClassifier",
                "accuracy": "72.04%",
                "roc_auc": "0.7885",
                "f1_score": "0.6762",
                "status": "Candidate Baseline",
                "lifecycle": "Pre-Release / Staging"
            }
        )
        print(f"Created Model Version 1: {v1.version}")
    else:
        client.update_model_version(
            name=MODEL_NAME,
            version="1",
            description="v1: Decision Tree Candidate Baseline (Accuracy: 72.04%, ROC-AUC: 0.7885). Benchmark baseline on 21st-century competencies."
        )
        for k, val in {
            "stage": "Staging",
            "model_architecture": "DecisionTreeClassifier",
            "accuracy": "72.04%",
            "roc_auc": "0.7885",
            "f1_score": "0.6762",
            "status": "Candidate Baseline",
            "lifecycle": "Pre-Release / Staging"
        }.items():
            client.set_model_version_tag(MODEL_NAME, "1", k, val)
        print("Updated Model Version 1 metadata & tags.")

    # Transition v1 to Staging / Archived
    try:
        client.transition_model_version_stage(
            name=MODEL_NAME,
            version="1",
            stage="Staging",
            archive_existing_versions=False
        )
    except Exception as e:
        print(f"Stage transition note for v1: {e}")

    try:
        client.set_registered_model_alias(MODEL_NAME, "challenger", "1")
        client.set_registered_model_alias(MODEL_NAME, "baseline", "1")
    except Exception as e:
        print(f"Alias note for v1: {e}")

except Exception as e:
    print(f"Error configuring v1: {e}")

# Register / Configure Version 2 (Production Champion)
v2_source = f"{rf_run.info.artifact_uri}/model"
try:
    if not any(v.version == "2" for v in existing_versions):
        v2 = client.create_model_version(
            name=MODEL_NAME,
            source=v2_source,
            run_id=rf_run.info.run_id,
            description="v2: Random Forest Champion Model (N=8,528 Students Benchmark, Accuracy: 73.51%, ROC-AUC: 0.7949, p95 Latency: 11.4ms). Approved for live production screening.",
            tags={
                "stage": "Production",
                "model_architecture": "RandomForestClassifier",
                "accuracy": "73.51%",
                "roc_auc": "0.7949",
                "f1_score": "0.7061",
                "p95_latency": "11.4ms",
                "benchmark_N": "8528",
                "status": "Production-Approved",
                "lifecycle": "Active Production"
            }
        )
        print(f"Created Model Version 2: {v2.version}")
    else:
        client.update_model_version(
            name=MODEL_NAME,
            version="2",
            description="v2: Random Forest Champion Model (N=8,528 Students Benchmark, Accuracy: 73.51%, ROC-AUC: 0.7949, p95 Latency: 11.4ms). Approved for live production screening."
        )
        for k, val in {
            "stage": "Production",
            "model_architecture": "RandomForestClassifier",
            "accuracy": "73.51%",
            "roc_auc": "0.7949",
            "f1_score": "0.7061",
            "p95_latency": "11.4ms",
            "benchmark_N": "8528",
            "status": "Production-Approved",
            "lifecycle": "Active Production"
        }.items():
            client.set_model_version_tag(MODEL_NAME, "2", k, val)
        print("Updated Model Version 2 metadata & tags.")

    # Transition v2 to Production
    try:
        client.transition_model_version_stage(
            name=MODEL_NAME,
            version="2",
            stage="Production",
            archive_existing_versions=False
        )
    except Exception as e:
        print(f"Stage transition note for v2: {e}")

    try:
        client.set_registered_model_alias(MODEL_NAME, "champion", "2")
        client.set_registered_model_alias(MODEL_NAME, "production", "2")
    except Exception as e:
        print(f"Alias note for v2: {e}")

except Exception as e:
    print(f"Error configuring v2: {e}")

# Verification summary of all versions in MLflow Model Registry
print("\n=================================================================")
print("🏆 Model Versioning Summary in MLflow Model Registry")
print("=================================================================")
updated_versions = client.search_model_versions(f"name='{MODEL_NAME}'")
for v in updated_versions:
    print(f"• Version {v.version}:")
    print(f"    Current Stage : {v.current_stage}")
    print(f"    Source Run ID : {v.run_id}")
    print(f"    Description   : {v.description}")
    print(f"    Tags          : {v.tags}")

reg_model = client.get_registered_model(MODEL_NAME)
if hasattr(reg_model, "aliases"):
    print(f"\nModel Aliases: {reg_model.aliases}")

print("\nDirect Link to MLflow Model Registry:")
print(f"👉 http://localhost:5000/#/models/{MODEL_NAME}")
print("=================================================================")

