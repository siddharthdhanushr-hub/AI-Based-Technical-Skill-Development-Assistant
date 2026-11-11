# AI-Based Technical Skill Development Assistant — Architecture

## 1. System Overview
The **AI-Based Technical Skill Development Assistant** is a personalized, topic-wise learning and readiness assessment application designed for students and technical learners. Unlike traditional learning management systems that rely on external forms or manual spreadsheet exports, this application collects learning interactions directly through the web platform as the student progresses through self-assessment, targeted revision, topic quizzes, and grip evaluation.

### Core Architecture Layers:
1. **Frontend Presentation Layer (React 19 + Vite)**
   - Topic & Subject Explorer
   - Topic Confidence Assessment (0–100 continuous slider)
   - Weak-Topic Targeted Revision (Concept summaries, definitions, examples, interactive flashcards)
   - Topic-Specific Quiz Engine (Item-by-item response, instant explanation, validated scoring)
   - Performance & Readiness Dashboard (Provisional vs. demonstrated grip, historical progress, next-step recommendations)
   - First-Party Telemetry & Event Logger

2. **Backend Services & API Layer (FastAPI + SQLAlchemy)**
   - RESTful API endpoints for curriculum, assessments, quizzes, telemetry, and grip calculations
   - Configurable business logic: Weak-topic threshold ($T_{\text{conf}} < 60$), Readiness scoring formulas
   - Deterministic rule-based baseline recommendations
   - Asynchronous telemetry logging preserving pseudonymous student identifiers

3. **Data & Persistence Layer (SQLite + CSV Event Store)**
   - Operational relational database (Subjects, Topics, Questions, Assessments, Attempts)
   - Append-only event store for first-party telemetry events
   - Sanitized training data pipelines feeding the ML workflows

4. **Machine Learning & MLOps Layer (DVC + MLflow + Scikit-Learn)**
   - Pre-quiz predictor pipeline (predicting topic mastery band without future score leakage)
   - DVC dataset versioning for raw, interim, and processed data artifacts
   - MLflow experiment tracking for baseline model comparisons (Dummy, Logistic Regression, Decision Tree, Random Forest)
   - Reproducible execution stages defined in `dvc.yaml`

---

## 2. End-to-End Learner Journey
```
[Select Course/Topic] 
       │
       ▼
[Self-Report Confidence (0-100)] ──► Log Event: confidence_assessment_submitted
       │
       ├─────────────────────────────────┐
  Confidence < 60                  Confidence >= 60
       │                                 │
       ▼                                 ▼
[Targeted Revision & Flashcards]   [Optional Direct Quiz Attempt]
       │                                 │
       └────────────────► ┌──────────────┘
                          │
                          ▼
                  [Take Topic Quiz] ──► Log Events: quiz_started, question_answered
                          │
                          ▼
                 [Submit & Instant Feedback] ──► Log Event: quiz_submitted, quiz_result_calculated
                          │
                          ▼
                [Topic Grip & Readiness]
               (Provisional / Developing /
                Needs Revision / Mastered)
                          │
                          ▼
              [Targeted Next Action Recommended]
```

---

## 3. Team Division & Workstream Architecture
| Workstream | Member | Focus Area | Deliverables |
|---|---|---|---|
| **Member 1** | Shreyas | Data Acquisition, Quality, EDA | `src/data_validation.py`, `01_dataset_acquisition_eda.ipynb`, `dataset_card.md`, `data_dictionary.md`, `dataset_approval_record.md`, bootstrap dataset |
| **Member 2** | Shreyash Singh | Feature Engineering, Baseline Models | `src/features.py`, `src/models/`, `02_feature_engineering_baselines.ipynb`, `initial_model_evaluation.md`, model benchmarks |
| **Member 3** | Siddharth Chandrashekar C | Student Frontend & Quiz Flow | React UI (confidence slider, revision, flashcards, quiz interface, results dashboard, progress tracking) |
| **Member 4** | Siddharth Dhanush R (Lead) | Backend Integration, API & MLOps | FastAPI endpoints, database persistence, DVC versioning, MLflow pipelines, `04_mlops_reproducibility.ipynb`, end-to-end integration |
