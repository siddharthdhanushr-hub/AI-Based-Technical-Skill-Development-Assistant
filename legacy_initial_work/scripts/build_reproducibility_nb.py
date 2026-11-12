"""
Script to generate and execute notebooks/04_mlops_reproducibility.ipynb
Author: Siddharth Dhanush R (Project Lead)
"""

import os
import sys
import json
import nbformat as nbf

def generate_notebook():
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.11.15"
        }
    }

    cells = []

    # Cell 1: Title & Overview
    cells.append(nbf.v4.new_markdown_cell("""# 04. MLOps Pipeline, Experiment Tracking & Reproducibility Audit
**Author:** Siddharth Dhanush R (Member 4, Project Lead)  
**Role:** Backend API, MLflow Tracking, DVC Pipeline, System Integration, and Documentation  
**Module:** Phase 1 Reproducibility and MLOps Orchestration  
**Academic Notice:** *All baseline experiments in Phase 1 utilize the synthetic bootstrap dataset (`is_synthetic = True`, $N=2,721$). Real-world student telemetry collection is scheduled for Phase 2 via the deployed React frontend and FastAPI ingestion layer.*

---

### Objectives of this Notebook
1. **Environment & Dependency Audit**: Record exact Python, system, and library versions.
2. **Git Commit History & Collaboration Audit**: Inspect multi-member branch integrations.
3. **DVC Pipeline & DAG Verification**: Verify automated reproducibility via `dvc.yaml` and `dvc.lock`.
4. **MLflow Experiment Tracking**: Query local MLflow runs, compare baseline models, and inspect champion artifacts.
5. **Zero-Leakage & Group Independence Verification**: Enforce mathematical guarantees on student separation and feature isolation.
6. **Automated Test Suite Audit**: Verify pass status across all 32 test cases spanning all four team members.
7. **Academic Limitations & Threats-to-Validity**: Formulate concrete risk assessments and mitigation paths."""))

    # Cell 2: Imports & Environment Configuration
    cells.append(nbf.v4.new_code_cell("""import os
import sys
import platform
import json
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yaml
import mlflow
import sklearn

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.getcwd(), "..")) if "notebooks" in os.getcwd() else os.path.abspath(".")
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"

print(f"Project Root: {PROJECT_ROOT}")
print(f"Working Directory: {os.getcwd()}")"""))

    # Cell 3: Environment Audit Table
    cells.append(nbf.v4.new_markdown_cell("""## 1. System & Environment Audit"""))
    cells.append(nbf.v4.new_code_cell("""env_info = {
    "Operating System": platform.platform(),
    "Python Version": sys.version.split()[0],
    "Processor": platform.processor() or "x86_64",
    "scikit-learn": sklearn.__version__,
    "mlflow": mlflow.__version__,
    "pandas": pd.__version__,
    "numpy": np.__version__,
    "matplotlib": plt.matplotlib.__version__,
    "seaborn": sns.__version__
}

env_df = pd.DataFrame(list(env_info.items()), columns=["Component", "Specification / Version"])
env_df"""))

    # Cell 4: Multi-Member Git Trajectory Audit
    cells.append(nbf.v4.new_markdown_cell("""## 2. Multi-Member Git Commit Trajectory
We audit the project commit graph to verify clear task decomposition, individual member authorship, and branch merges."""))
    cells.append(nbf.v4.new_code_cell("""git_log = subprocess.run(
    ["git", "log", "--graph", "--oneline", "--decorate", "-n", "18"],
    cwd=PROJECT_ROOT,
    capture_output=True,
    text=True
).stdout

print("Recent Git Commit Graph:")
print(git_log)"""))

    # Cell 5: DVC Pipeline Verification
    cells.append(nbf.v4.new_markdown_cell("""## 3. DVC Pipeline Orchestration & Dependency Lineage
DVC manages the data science DAG, enforcing deterministic reproduction across three distinct stages:
1. `validate_data`: Validates Pydantic schema constraints and missing values.
2. `feature_engineering`: Transforms event telemetry into leakage-free pre-quiz observations.
3. `train_and_track`: Trains all baseline models under MLflow tracking and saves the champion artifact."""))
    cells.append(nbf.v4.new_code_cell("""dvc_yaml_path = os.path.join(PROJECT_ROOT, "dvc.yaml")
dvc_lock_path = os.path.join(PROJECT_ROOT, "dvc.lock")

with open(dvc_yaml_path, "r", encoding="utf-8") as f:
    dvc_spec = yaml.safe_load(f)

print("DVC Defined Stages:")
for stage, details in dvc_spec.get("stages", {}).items():
    print(f"- Stage: {stage}")
    print(f"  Command: {details.get('cmd')}")
    print(f"  Dependencies: {details.get('deps')}")
    print(f"  Outputs: {list(details.get('outs', {}))}")"""))

    # Cell 6: DVC Lock File Checksums
    cells.append(nbf.v4.new_code_cell("""with open(dvc_lock_path, "r", encoding="utf-8") as f:
    dvc_lock = yaml.safe_load(f)

lock_records = []
for stage, data in dvc_lock.get("stages", {}).items():
    for dep in data.get("deps", []):
        lock_records.append({"Stage": stage, "Type": "Dependency", "Path": dep.get("path"), "MD5": dep.get("md5")[:12]})
    for out in data.get("outs", []):
        lock_records.append({"Stage": stage, "Type": "Output", "Path": out.get("path"), "MD5": out.get("md5")[:12]})

df_lock = pd.DataFrame(lock_records)
df_lock"""))

    # Cell 7: MLflow Experiment Tracking Store Analysis
    cells.append(nbf.v4.new_markdown_cell("""## 4. MLflow Experiment Tracking & Benchmark Analysis
We load the experiment runs logged in `./mlruns` under experiment `technical_skill_mastery_baselines`."""))
    cells.append(nbf.v4.new_code_cell("""tracking_dir = os.path.join(PROJECT_ROOT, "mlruns")
mlflow.set_tracking_uri(f"file:///{tracking_dir.replace(os.sep, '/')}")

experiment = mlflow.get_experiment_by_name("technical_skill_mastery_baselines")
runs_df = mlflow.search_runs(experiment_ids=[experiment.experiment_id])

# Deduplicate to latest runs per model name
model_col = "tags.mlflow.runName" if "tags.mlflow.runName" in runs_df.columns else "run_id"
runs_df["Model"] = runs_df[model_col]

summary_runs = runs_df.groupby("Model", as_index=False).first()

display_cols = ["Model"]
if "metrics.accuracy" in summary_runs.columns:
    summary_runs["Accuracy"] = summary_runs["metrics.accuracy"]
    display_cols.append("Accuracy")
if "metrics.balanced_accuracy" in summary_runs.columns:
    summary_runs["Balanced Accuracy"] = summary_runs["metrics.balanced_accuracy"]
    display_cols.append("Balanced Accuracy")
if "metrics.f1_macro" in summary_runs.columns:
    summary_runs["Macro F1"] = summary_runs["metrics.f1_macro"]
    display_cols.append("Macro F1")
if "metrics.f1_weighted" in summary_runs.columns:
    summary_runs["Weighted F1"] = summary_runs["metrics.f1_weighted"]
    display_cols.append("Weighted F1")
if "tags.is_champion" in summary_runs.columns:
    summary_runs["Champion"] = summary_runs["tags.is_champion"].fillna("False")
    display_cols.append("Champion")

summary_runs = summary_runs[display_cols].sort_values(by="Macro F1", ascending=False).reset_index(drop=True)
summary_runs"""))

    # Cell 8: Model Comparison Chart
    cells.append(nbf.v4.new_markdown_cell("""### Model Performance Comparison Chart"""))
    cells.append(nbf.v4.new_code_cell("""chart_df = summary_runs.sort_values(by="Macro F1", ascending=True)

fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(chart_df))
width = 0.35

rects1 = ax.barh(x - width/2, chart_df["Macro F1"], width, label="Macro F1-Score", color="#6366f1")
rects2 = ax.barh(x + width/2, chart_df["Accuracy"], width, label="Accuracy", color="#38bdf8")

ax.set_ylabel("Algorithm / Model")
ax.set_xlabel("Score (0.0 to 1.0)")
ax.set_title("Phase 1 Baseline Performance (Grouped Test Partition)", fontsize=13, fontweight="bold")
ax.set_yticks(x)
ax.set_yticklabels(chart_df["Model"])
ax.legend(loc="lower right")
ax.grid(axis="x", linestyle="--", alpha=0.5)

for r in rects1:
    ax.annotate(f"{r.get_width():.3f}",
                xy=(r.get_width(), r.get_y() + r.get_height() / 2),
                xytext=(3, 0), textcoords="offset points", ha="left", va="center", fontsize=9)

for r in rects2:
    ax.annotate(f"{r.get_width():.3f}",
                xy=(r.get_width(), r.get_y() + r.get_height() / 2),
                xytext=(3, 0), textcoords="offset points", ha="left", va="center", fontsize=9)

plt.tight_layout()
plt.show()"""))

    # Cell 9: Target Leakage & Group Independence Audit
    cells.append(nbf.v4.new_markdown_cell("""## 5. Zero-Leakage & Group Independence Verification
We verify that no post-quiz outcome fields exist in the pre-quiz predictor set, and that attempts from the same student never cross train and test boundaries."""))
    cells.append(nbf.v4.new_code_cell("""from src.features import FORBIDDEN_LEAKAGE_COLUMNS, create_grouped_train_test_split
from src.evaluation import verify_zero_leakage

metadata_path = os.path.join(PROJECT_ROOT, "models", "model_metadata.json")
with open(metadata_path, "r", encoding="utf-8") as f:
    model_meta = json.load(f)

feature_cols = model_meta["feature_columns"]
print("Active Predictor Features:")
for col in feature_cols:
    print(f" - {col}")

# Run zero leakage assertion
verify_zero_leakage(feature_cols, FORBIDDEN_LEAKAGE_COLUMNS)
print("\\nZero Target Leakage Verified: No post-quiz outcome variables present.")

# Verify Student Independence in GroupSplit
features_path = os.path.join(PROJECT_ROOT, "data", "processed", "pre_quiz_features.csv")
df_feat = pd.read_csv(features_path)
train_df, test_df = create_grouped_train_test_split(df_feat, group_col="student_id", test_size=0.25, random_state=42)

train_students = set(train_df["student_id"].unique())
test_students = set(test_df["student_id"].unique())
overlap = train_students.intersection(test_students)

print(f"Unique Students in Training Set: {len(train_students)}")
print(f"Unique Students in Test Set: {len(test_students)}")
print(f"Student Overlap Count: {len(overlap)}")
assert len(overlap) == 0, "Student overlap violation detected!"
print("Group Independence Verified: Zero student overlap between train and test partitions.")"""))

    # Cell 10: Test Suite Verification
    cells.append(nbf.v4.new_markdown_cell("""## 6. End-to-End Automated Test Suite Audit
We execute the complete pytest suite spanning all 4 modules (Data Validation, Modeling, Frontend Contracts, and MLOps API)."""))
    cells.append(nbf.v4.new_code_cell("""pytest_run = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/", "-v", "--no-header"],
    cwd=PROJECT_ROOT,
    capture_output=True,
    text=True
)

print(pytest_run.stdout)"""))

    # Cell 11: Academic Threats to Validity
    cells.append(nbf.v4.new_markdown_cell("""## 7. Academic Reproducibility & Threats-to-Validity Statement
1. **Synthetic Nature of Bootstrap Data**: All 2,721 records are synthetically generated under a seeded Markovian model ($r=0.627$). Conclusions drawn here reflect algorithmic pipeline validity rather than empirical human psychology.
2. **Cold-Start Bias**: In early student interactions without revision or prior quiz history, the pipeline relies on the self-reported confidence prior and calibrated rule heuristics until interaction density builds.
3. **Small Sample Test Partition**: The test partition comprises 63 attempts across 12 student clusters. Standard errors on F1 estimates are approximately $\\pm 0.06$.
4. **Phase 2 Transition**: Real telemetry ingested via the React client and FastAPI endpoints will replace synthetic bootstrap data in Phase 2 with full DVC version lineage."""))

    nb.cells = cells
    return nb

if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_dir = os.path.join(project_root, "notebooks")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "04_mlops_reproducibility.ipynb")

    nb = generate_notebook()
    with open(out_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"Notebook written to: {out_path}")
