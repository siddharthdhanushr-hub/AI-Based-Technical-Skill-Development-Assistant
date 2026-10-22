# Shared Project Contribution Tracker — Phase 1

This tracker documents individual ownership, specific tasks, implementation evidence, and status across all four project team members.

---

## Team Roster
- **Member 1 — Shreyas**: Data Acquisition, Data Quality, Schema Validation, and Exploratory Data Analysis.
- **Member 2 — Shreyash Singh**: Feature Engineering, Baseline Modeling, Model Comparison, and Evaluation.
- **Member 3 — Siddharth Chandrashekar C**: Student-Facing Learning Interface, Revision/Flashcards, and Quiz Experience.
- **Member 4 — Siddharth Dhanush R (Project Lead)**: Central Integration, Backend Orchestration, MLOps, DVC, and MLflow Reproducibility.

---

## Workstream Activity Log

| Member | Task ID | Task Title | Status | Branch | Deliverables & Artifacts | Evidence & Notes |
|---|---|---|---|---|---|---|
| **Member 4** | ARCH-01 | Architecture, Contracts, & Base Scaffold | **Done** | `main` | `docs/architecture.md`, `docs/api_contract.md`, `docs/data_schema.md`, `frontend/`, `requirements.txt`, `.gitignore` | Initialized repository foundation, contracts, and frontend reference scaffold (Commit: `4b1c9e7`). |
| **Member 1** | DATA-01 | Interaction Event Schema & Quality Validator | **Done** | `feature/data-acquisition-eda` | `src/data_validation.py`, `tests/test_data_validation.py` | Pydantic schema validation, range checks, duplicate detection. 10/10 unit tests passing (PR #1 Merged). |
| **Member 1** | DATA-02 | Bootstrap Dataset Generation (Explicit Synthetic) | **Done** | `feature/data-acquisition-eda` | `data/raw/student_interactions_bootstrap.csv`, `src/data/generate_bootstrap_dataset.py` | 2,721 simulated learning events across 50 students and 6 topics with `is_synthetic=True`. |
| **Member 1** | DATA-03 | Exploratory Data Analysis (EDA) Notebook | **Done** | `feature/data-acquisition-eda` | `notebooks/01_dataset_acquisition_eda.ipynb` | Fully executed Jupyter notebook with distributions, correlation analysis ($r=0.627$), and calibration gap charts. |
| **Member 1** | DATA-04 | Dataset Documentation & Approval Record | **Done** | `feature/data-acquisition-eda` | `reports/dataset_card.md`, `reports/data_dictionary.md`, `reports/dataset_approval_record.md` | Comprehensive data dictionary, dataset card, and Phase 1 ethical approval record. |
| **Member 2** | ML-01 | Feature Engineering & Leakage-Free Preprocessing | **Done** | `feature/feature-engineering-baselines` | `src/features.py`, `data/processed/pre_quiz_features.csv`, `tests/test_features_models.py` | Extracted pre-quiz feature matrix with zero target leakage. GroupShuffleSplit by student. (PR #2 Merged). |
| **Member 2** | ML-02 | Baseline Model Comparison & Evaluation | **Done** | `feature/feature-engineering-baselines` | `src/models/baseline_models.py`, `src/models/predictor.py`, `models/mastery_classifier.joblib`, `02_feature_engineering_baselines.ipynb`, `reports/initial_model_evaluation.md` | Trained and compared Dummy, Logistic Regression, Decision Tree, Random Forest. Logistic Regression selected (Macro-F1: 0.5268). |
| **Member 3** | UI-01 | Student Dashboard & Topic Explorer | **Done** | `feature/frontend-learning-flow` | `frontend/src/pages/Dashboard.jsx`, `TopicSelection.jsx` | Subject & topic browsing, course navigation, and readiness summary cards. |
| **Member 3** | UI-02 | Confidence Assessment & Revision Flow | **Done** | `feature/frontend-learning-flow` | `ConfidenceAssessment.jsx`, `RevisionView.jsx` | 0–100 confidence slider, 3D interactive flashcards with Space/Arrow keyboard navigation. |
| **Member 3** | UI-03 | Interactive Quiz Engine & Feedback | **Done** | `feature/frontend-learning-flow` | `QuizView.jsx`, `PerformanceAnalytics.jsx`, `tests/test_frontend_contracts.py`, `reports/frontend_usage_guide.md` | Question player, instant explanation, score calculation, retake tracking, and calibration analytics. 19/19 tests passing. |
| **Member 4** | MLOPS-01 | DVC Dataset Versioning & Pipeline | **Todo** | `feature/backend-mlops-integration` | `dvc.yaml`, `dvc.lock`, `.dvc/config` | Planned: Reproducible DVC pipeline stages (`validate`, `preprocess`, `train`). |
| **Member 4** | MLOPS-02 | MLflow Experiment Tracking & Logging | **Todo** | `feature/backend-mlops-integration` | `src/mlflow_utils.py`, `notebooks/04_mlops_reproducibility.ipynb` | Planned: Local MLflow tracking of runs, parameters, metrics, artifacts. |
| **Member 4** | INT-01 | FastAPI Endpoints & Database Persistence | **Todo** | `feature/backend-mlops-integration` | `backend/main.py`, `backend/routes/`, `backend/models/` | Planned: REST API connecting frontend to data store and model inference. |
