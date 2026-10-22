# AI-Based Technical Skill Development Assistant

[![Phase 1 Status](https://img.shields.io/badge/Phase%201-In%20Progress-blue)](https://github.com/siddharthdhanushr-hub/AI-Based-Technical-Skill-Development-Assistant)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![React 19](https://img.shields.io/badge/react-19.2-61dafb.svg)](https://react.dev/)

An intelligent, topic-wise learning and readiness assessment platform that combines first-party learning interaction telemetry, student self-assessment, focused revision with flashcards, topic quizzes, transparent grip scoring, and reproducible machine learning workflows.

---

## 1. Project Overview & Motivation
Traditional education tools either depend on passive self-assessments (which often suffer from the Dunning-Kruger effect or uncalibrated confidence) or generic quizzes that lack targeted remediation. Furthermore, learning data is frequently collected through detached Google Forms or spreadsheets, severing the link between real-time learner behavior and predictive modeling.

The **AI-Based Technical Skill Development Assistant** addresses this by:
1. Collecting fine-grained learning events (confidence ratings, revision activity, time per question, attempts) directly through the website during natural usage.
2. Distinguishing **Confidence** (self-reported), **Quiz Performance** (demonstrated mastery), and **Topic Grip** (evidence-based synthesized readiness).
3. Providing immediate, targeted revision (concept summaries, definitions, interactive flashcards) before quizzes for topics below a configurable confidence threshold ($T_{\text{conf}} < 60$).
4. Supporting a reproducible MLOps lifecycle with **Git**, **DVC** dataset versioning, **MLflow** experiment tracking, and leakage-free baseline model evaluation.

---

## 2. Four-Member Team Workstreams
The engineering work is divided into four distinct modules:

| Member | Primary Focus | Key Responsibilities |
|---|---|---|
| **Member 1 (Shreyas)** | Data Acquisition, Quality & EDA | Event schema definition, quality validation, bootstrap dataset generation, exploratory data analysis, data dictionary & dataset card. |
| **Member 2 (Shreyash Singh)** | Feature Engineering & Baselines | Pre-quiz feature extraction, target leakage prevention, baseline model training (Dummy, Logistic Regression, Decision Tree, Random Forest), evaluation metrics. |
| **Member 3 (Siddharth Chandrashekar C)** | Student Frontend & Quiz Flow | Course explorer, confidence assessment slider, targeted revision with flashcards, topic quiz engine, results dashboard. |
| **Member 4 (Siddharth Dhanush R, Lead)** | Architecture, Integration & MLOps | API contracts, FastAPI backend, SQLite database persistence, DVC pipeline orchestration, MLflow experiment tracking, reproducibility documentation. |

---

## 3. Directory Layout
```text
AI-Based-Technical-Skill-Development-Assistant/
├── backend/                  # FastAPI backend and persistence services
├── frontend/                 # React 19 + Vite student application
│   ├── src/
│   │   ├── pages/            # Dashboard, TopicSelection, ConfidenceAssessment, RevisionView, QuizView
│   │   ├── api.js            # Axios client with fallback support
│   │   └── index.css         # Modern design tokens and utility styles
│   ├── package.json
│   └── vite.config.js
├── src/                      # Reusable Python modules
│   ├── data_validation.py    # Schema & data quality validation (Member 1)
│   ├── data/                 # Dataset generation & processing utilities
│   ├── features/             # Feature engineering pipelines (Member 2)
│   └── models/               # Model training & inference wrappers (Member 2)
├── data/
│   ├── raw/                  # Versioned raw event datasets (DVC tracked)
│   └── processed/            # Engineered feature matrices
├── notebooks/
│   ├── 01_dataset_acquisition_eda.ipynb      # EDA & quality analysis (Member 1)
│   ├── 02_feature_engineering_baselines.ipynb# Model training & evaluation (Member 2)
│   └── 04_mlops_reproducibility.ipynb        # Reproducibility audit & MLOps (Member 4)
├── reports/
│   ├── dataset_card.md                       # Comprehensive dataset provenance (Member 1)
│   ├── data_dictionary.md                    # Attribute descriptions & bounds (Member 1)
│   ├── dataset_approval_record.md            # Ethical & academic approval (Member 1)
│   ├── initial_model_evaluation.md           # Baseline benchmarks (Member 2)
│   └── reproducibility_report.md             # End-to-end MLOps audit (Member 4)
├── tests/
│   ├── test_data_validation.py               # Data quality unit tests (Member 1)
│   └── test_api.py                           # Integration API tests (Member 4)
├── docs/
│   ├── architecture.md                       # System architecture specification
│   ├── api_contract.md                       # Shared REST API contracts
│   ├── data_schema.md                        # Telemetry schema definitions
│   └── contribution_tracker.md               # Member-wise task status
├── requirements.txt                          # Python dependencies
└── dvc.yaml                                  # DVC reproducible pipeline stages
```

---

## 4. Quickstart & Setup Guide

### Python Environment (Backend & ML)
```bash
# Clone the repository
git clone https://github.com/siddharthdhanushr-hub/AI-Based-Technical-Skill-Development-Assistant.git
cd AI-Based-Technical-Skill-Development-Assistant

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run data quality tests
pytest tests/test_data_validation.py -v
```

### Frontend Environment (Learner Portal)
```bash
cd frontend
npm install
npm run dev
```

---

## 5. Phase 1 Academic Verification
- **Submission Window History**: Original academic review window: 13–17 October 2026; revised submission date awaiting confirmation.
- **Dataset Provenance**: Phase 1 utilizes an approved synthetic bootstrap dataset (`student_interactions_bootstrap.csv`) to resolve the cold-start problem before real students log into the platform. Real student telemetry is recorded directly into the event store during live usage.
