# Dataset Acquisition & Approval Record — Phase 1

This formal approval record documents the origin, governance, quality inspection, and academic approval status of datasets utilized in Phase 1.

---

## 1. Dataset Identification
- **Dataset Title**: Phase 1 Bootstrap Interaction Telemetry
- **Filename**: `student_interactions_bootstrap.csv`
- **Location**: `data/raw/student_interactions_bootstrap.csv`
- **SHA-256 Checksum**: Documented under DVC metadata
- **Acquisition Date**: October 2026
- **Prepared By**: Member 1 (Shreyas — Data Acquisition & Quality Owner)
- **Reviewed By**: Member 4 (Siddharth Dhanush R — Project Lead)

---

## 2. Provenance & Generation Method
- **Method**: Generative synthetic bootstrap via deterministic simulation script (`src/data/generate_bootstrap_dataset.py`, `seed=42`).
- **Academic Justification**: The project migrated from an offline classification tool to a direct web-telemetry system. A cold-start bootstrap dataset is required to validate data validation scripts, feature engineering, baseline models, and DVC/MLflow pipelines before empirical classroom data is accumulated.
- **Real Learner Data Policy**: In accordance with project requirements, no unconsented real student observations or manual Google Forms spreadsheets are ingested. Real learner telemetry will be captured solely through the active web application subject to user consent.

---

## 3. Data Quality & Hygiene Sign-Off

| Quality Check | Inspection Standard | Verification Result | Sign-Off |
|---|---|---|---|
| **Schema Completeness** | All mandatory columns present | 15 / 15 columns verified | **PASS** |
| **Duplicate Check** | Unique `event_id` keys | 0 duplicates found across 2,721 rows | **PASS** |
| **Range Bounds** | `confidence_score` $\in [0, 100]$, `quiz_score` $\in [0, 100]$ | 0 out-of-bounds violations | **PASS** |
| **Time Hygiene** | Response times $\ge 0.0$ seconds | 0 negative durations | **PASS** |
| **Synthetic Flagging** | Clear provenance marker | 100% of rows marked `is_synthetic=True` | **PASS** |
| **Target Independence** | Leakage prevention checks | Pre-quiz and post-quiz fields explicitly isolated | **PASS** |

---

## 4. Phase 1 Review Status
- **Initial Development Approval**: Approved for internal Phase 1 baseline modeling and MLOps testing.
- **Review Deadlines**: Original review window 13–17 October 2026; revised review date awaiting final confirmation from the instructor.
- **Formal Sign-Off**:
  - *Data Acquisition Lead*: Shreyas (Member 1) — Signed: 2026-10-23
  - *Project Integration Lead*: Siddharth Dhanush R (Member 4) — Signed: 2026-10-23
