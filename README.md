# AI-Based Technical Skill Development Assistant

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18.x-61DAFB.svg?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.x-646CFF.svg?logo=vite&logoColor=white)](https://vitejs.dev/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-MLOps-F7931E.svg?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![MLflow](https://img.shields.io/badge/MLflow-Registry-0194E2.svg?logo=mlflow&logoColor=white)](https://mlflow.org/)
[![DVC](https://img.shields.io/badge/DVC-Data%20Version%20Control-945DD6.svg?logo=dvc&logoColor=white)](https://dvc.org/)

An enterprise-grade, full-stack MLOps platform for technical competency screening, adaptive skill development, and career readiness validation. Designed specifically for students and engineering professionals preparing for modern technical recruitment screenings (HackerRank, CodeSignal, LeetCode, and AMCAT style assessments).

---

## 🌟 Key Features & Innovations

### 1. 21st-Century Competency Gating Engine
- Evaluates candidate self-reported proficiencies (0–6 scale) across **10 modern technical competencies**:
  1. `ai_ml`: Artificial Intelligence & Machine Learning
  2. `data_science`: Data Science, Big Data & Analytics
  3. `software_development`: Full-Stack & Cloud Application Engineering
  4. `programming_skills`: Algorithms, Data Structures & Asymptotic Efficiency
  5. `cyber_security`: Security Engineering, OWASP & DevSecOps
  6. `distributed_computing_systems`: Cloud, Containers & Microservices
  7. `database_fundamentals`: Modern Relational & NoSQL Data Stores
  8. `software_engineering`: Clean Code, Automated Testing & CI/CD Pipelines
  9. `troubleshooting_skills`: Observability, SRE & Production Root-Cause Analysis
  10. `technical_communication`: Agile Collaboration, RFCs & Code Reviews
- **Champion Machine Learning Model:** Evaluated on an $N = 8,528$ benchmark student dataset (CareerMap, Mendeley Data, DOI: 10.17632/5z68cvxssn.1).
- **Champion Model:** **Random Forest** (100 de-correlated trees, `max_depth=7`) achieving **73.51% Accuracy** and **0.795 ROC-AUC**.

### 2. Dual-Branch Adaptive Routing
```
                                [Student Self-Assessment]
                                           │
                             (MLOps Champion Random Forest)
                                           │
                          ┌────────────────┴────────────────┐
                          ▼                                 ▼
             [Pass Probability ≥ 50%]          [Pass Probability < 50%]
               (Above Threshold)                 (Below Threshold / Gaps)
                          │                                 │
                          ▼                                 ▼
               [Direct Cross-Verification]       [Auto-Sync to Skill Tracker]
               10 Screening Questions            Review Briefs, Flashcards,
               Immediate Validation              Key Heuristics & Projects
                                                            │
                                                            ▼
                                                 [Take Cross-Verification]
```
- **Branch A — Above Threshold ($P \ge 50\%$):** 
  Directly unlocks the **21st-Century Cross-Verification Exam (10 Questions)** to validate claimed proficiencies against objective industry screening questions.
- **Branch B — Below Threshold ($P < 50\%$ / Skill Gaps):**
  Identifies exact role-specific gaps ($G_i = \max(0, R_i - S_i)$ across 16 career profiles) and automatically syncs them into the **Skill Tracker**. Students review **Comprehensive Skill Briefs**, **Interactive Flashcards**, and generate **Production Portfolio Projects** before taking the verification exam.

### 3. Full-Stack Web Application Suite
- **Vibrant Glassmorphism Frontend:** Modern, responsive UI with real-time feedback, interactive sliders, and PDF report downloads.
- **Skill Manager:** AI document ingestion (PDF, Word, Images, OCR) with automatic extraction of pure technical competencies (excluding administrative boilerplate).
- **Skill Tracker:** Interactive competency checklist, portfolio project idea generator, customized study roadmaps, and instant flashcard drills.
- **Performance Analytics & Quiz Engine:** 10-question adaptive skill assessments with difficulty weighting, response time tracking, and remedial recommendations.

### 4. MLOps Governance & Architectural Insights
- **Phase 1 Benchmark Evaluation:** Comparative leaderboard against Decision Trees ($72.04\%$) and Logistic Regression ($73.45\%$), complete Confusion Matrix breakdown ($TN=711, FP=210, FN=242, TP=543$), and probabilistic label engineering documentation.
- **Phase 2 Productionization Deliverables:** 
  - Behavioral quality tests ($100\%$ pass rate across Boundary, Monotonicity, Invariance, and Latency benchmarks).
  - Evaluator directive justification matrix (curating the 10 modern competencies and pruning 7 legacy hardware/waterfall domains).
  - MLflow Model Registry integration and DVC pipeline tracking.

---

## 📁 Repository Structure

```
.
├── backend/
│   ├── ai/                   # AI extraction, flashcards, quizzes, project generator
│   ├── core/                 # Database, configuration, authentication, CSV exporters
│   ├── data/                 # Benchmark data, student assessments, weak topic logs
│   ├── ml/                   # Legacy analytics and ML prediction bridges
│   ├── mlops/                # MLOps service, routes, 21st-century constants & schemas
│   ├── mlops_models/         # Serialized models (random_forest.joblib, registry manifests)
│   ├── mlops_reports/        # Phase 1 & 2 evaluation reports, metrics.json, model risk cards
│   ├── syllabus/             # Skill track management and competency CRUD routes
│   ├── user/                 # Authentication, authorization, student profiles
│   ├── main.py               # FastAPI application entrypoint
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── CenturySkillsAssessment.jsx  # 21st-Century self-assessment & verification
│   │   │   ├── MLOpsInsights.jsx            # Detailed Phase 1 & Phase 2 report dashboard
│   │   │   ├── Dashboard.jsx                # Main command center & featured hero banner
│   │   │   ├── SkillManager.jsx             # AI syllabus & skill upload manager
│   │   │   ├── StudyTracker.jsx             # Competency tracker, projects & flashcards
│   │   │   ├── QuizSession.jsx              # 10-Question assessment session
│   │   │   └── PerformanceAnalytics.jsx     # Longitudinal competency analytics
│   │   ├── api.js                           # Axios API client with automatic JWT handling
│   │   └── App.jsx                          # Root routes & navigation bar
│   ├── package.json                         # Frontend dependencies (React 18, Vite)
│   └── vite.config.js                       # Vite build configuration
├── Project_Report/           # Comprehensive software design specifications & diagrams
├── legacy_initial_work/      # Archive of early baseline experiments and EDA deliverables
└── README.md
```

---

## ⚡ Quickstart Guide

### Prerequisites
- **Python:** 3.11 or higher
- **Node.js:** 18.x or higher
- **Package Managers:** `pip` and `npm`

---

### 1. Backend Setup

```bash
# Navigate to the repository root
cd AI-Based-Technical-Skill-Development-Assistant

# Create and activate virtual environment
python -m venv .venv

# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Start the FastAPI backend server
uvicorn backend.main:app --host 0.0.0.0 --port 8005 --reload
```
The FastAPI backend and OpenAPI docs will be available at:
- **API Base:** `http://localhost:8005`
- **Interactive Swagger Docs:** `http://localhost:8005/docs`

---

### 2. Frontend Setup

```bash
# Open a new terminal in the repository root
cd frontend

# Install npm dependencies
npm install

# Start Vite dev server
npm run dev
```
The web application will launch at:
- **Frontend URL:** `http://localhost:5173`

---

## 🔌 Core API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/mlops/config` | Returns 21st-century competency taxonomy, roles, and rating scales |
| `POST` | `/api/mlops/evaluate` | Evaluates student confidence vector via Random Forest Champion model |
| `POST` | `/api/mlops/sync-tracker` | Proactively syncs identified skill gaps into the student's Skill Tracker |
| `GET` | `/api/mlops/verification-quiz` | Returns the 10-question cross-verification screening assessment |
| `GET` | `/api/mlops/insights` | Delivers Phase 1 benchmark metrics and Phase 2 MLOps governance data |
| `GET` | `/api/syllabus/subjects` | Retrieves user's active skill tracks and competencies |
| `POST` | `/api/ai/syllabus/extract/{id}` | Ingests document/image and extracts clean technical competencies |
| `POST` | `/api/ai/project-ideas/{id}` | Generates industry portfolio projects with tech stacks and resume impact |
| `POST` | `/api/ai/quiz/generate` | Generates 10-question adaptive technical quiz |

---

## 🛡️ Model Governance & Evaluation Summary

| Metric | Random Forest (Champion) | Logistic Regression | Decision Tree |
| :--- | :---: | :---: | :---: |
| **Accuracy** | **73.51%** | 73.45% | 72.04% |
| **ROC-AUC** | **0.7949** | 0.7974 | 0.7885 |
| **F1-Score** | **0.7061** | 0.7113 | 0.6762 |
| **Precision** | **0.7211** | 0.7117 | 0.7238 |
| **Recall** | **0.6917** | 0.7108 | 0.6344 |
| **Inference Latency** | **< 12 ms** (p95) | < 5 ms | < 5 ms |

> **Audit Note:** The early exploratory scripts and baseline Phase 1 prototypes are archived in [`/legacy_initial_work/`](./legacy_initial_work/) for full historical traceability. All active production services run exclusively from the root workspace.

---

## 👥 Authors & Team Contributors
- **AI-Based Technical Skill Development Assistant Team**
- Integration & MLOps Productionization: Siddharth Dhanush R & Team
